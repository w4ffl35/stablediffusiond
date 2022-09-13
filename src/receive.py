#!/usr/bin/env python
"""
Starts a queue consumer that receives messages and runs stables diffusion.
"""

import sys
import os
import json
try:
    from classes.txt2img import Txt2Img
    from classes.img2img import Img2Img
except ImportError:
    print("Unable to import classes. Please install requirements.")
    Txt2Img = None
    Img2Img = None

try:
    from stablediffusiond.settings import SCRIPTS
except ImportError:
    print("Unable to import settings file. Please create a settings.py file.")
    SCRIPTS = {}

from connect import connect_queue, start_consumer, publish_queue, disconnect_queue
import logger as log


class Receiver:
    """
    Loads stable diffusion model, watches a queue, runs the model and enqueues the results.
    """
    model = None
    device = None
    _txt2img_loader = None
    _img2img_loader = None

    @property
    def txt2img_loader(self):
        """
        Loads the txt2img model
        :return: Txt2Img instance
        """
        return self._txt2img_loader

    @property
    def img2img_loader(self):
        """
        Loads the img2img model
        :return: Img2Img instance
        """
        return self._img2img_loader

    def process_data_value(self, key, value):
        """
        Process the data value. Ensure that we use the correct types.
        :param key: key
        :param value: value
        :return: processed value
        """
        if value == "true":
            return True
        if value == "false":
            return False
        if key in [
            "ddim_steps", "n_iter", "H", "W", "C", "f",
            "n_samples", "n_rows", "seed"
        ]:
            return int(value)
        if key in ["ddim_eta", "scale", "strength"]:
            return float(value)
        return value


    def enqueue_results(self, saved_files):
        """
        Enqueue the results in the results queue
        :param saved_files: list of saved files
        :return: None
        """
        log.info("Enqueuing results")
        connection, channel = connect_queue("response_queue")
        publish_queue(channel, json.dumps(saved_files), "response_queue")
        disconnect_queue(connection, "response_queue")

    def decode_binary_string(self, message):
        """
        Decode a binary string to a string, or returns original string if unable to decode.
        :param message: binary string
        :return: string
        """
        try:
            # This is temporary. We will be switching to capnproto soon.
            message = ''.join(
                chr(
                    int(message[i * 8:i * 8 + 8], 2)
                ) for i in range(len(message) // 8)
            )
        except ValueError as exception:
            log.warning(f"Unable to decode binary string. Returning original string. {exception}")
        return message


    def callback(self, _channel, _method, _properties, body):
        """
        This function is called when a message is received on the queue.
        :param _channel: channel
        :param _method: method
        :param _properties: properties
        :param body: body
        :return: None
        """
        # decode body from binary to string
        body = self.decode_binary_string(body)
        data = json.loads(body)

        log.info(" [x] Received request")

        log.info(" Running stable diffusion sample...")
        script_type = data.get("type", "txt2img")
        options = SCRIPTS[script_type]

        # get all keys from data
        keys = data.keys()

        for index, opt in enumerate(options):
            if opt[0] in keys:
                options[index] = (opt[0], self.process_data_value(opt[0], data.get(opt[0], opt[1])))

        if script_type == "txt2img":
            saved_files = self.txt2img_loader.sample(options=options)
        else:
            saved_files = self.img2img_loader.sample(options=options)

        self.enqueue_results(saved_files)

        log.info("Completed")

    def __init__(self):
        """
        Constructor, starts a consumer on the queue.
        """

        self._txt2img_loader = Txt2Img(
            options=SCRIPTS["txt2img"],
            model=self.model,
            device=self.device
        )

        self._img2img_loader = Img2Img(
            options=SCRIPTS["img2img"],
            model=self._txt2img_loader.model,
            device=self._txt2img_loader.device
        )

        try:
            _connection, channel = connect_queue("request_queue")
            start_consumer(channel, self.callback, "request_queue")
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)


if __name__ == "__main__":
    Receiver()
