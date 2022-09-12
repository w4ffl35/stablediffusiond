#!/usr/bin/env python
import sys
import os
import json
import logger as log
from connect import connect_queue, start_consumer, publish_queue, disconnect_queue
from settings import SCRIPTS

# import settings and set path for script imports
from settings import GENERAL

SCRIPTS_ROOT = GENERAL["sd_scripts"]
PYTHON_PATH = GENERAL["sd_python_path"]
sys.path.append(os.path.dirname(os.path.dirname(SCRIPTS_ROOT)))
sys.path.append(os.path.dirname(os.path.join(os.path.dirname(SCRIPTS_ROOT), "..")))

from classes.txt2img import Txt2Img
from classes.img2img import Img2Img


class Receiver:
    model = None
    device = None
    _txt2img_loader = None
    _img2img_loader = None

    @property
    def txt2img_loader(self):
        if not self._txt2img_loader:
            self._txt2img_loader = Txt2Img(options=SCRIPTS["txt2img"], model=self.model, device=self.device)
        return self._txt2img_loader

    @property
    def img2img_loader(self):
        if not self._txt2img_loader:
            self._img2img_loader = Img2Img(options=SCRIPTS["img2img"], model=self.model, device=self.device)
        return self._txt2img_loader

    def process_data_value(self, key, value):
        if value == "true":
            return True
        elif value == "false":
            return False
        elif [
            "ddim_steps", "n_iter", "H", "W", "C", "f",
            "n_samples", "n_rows", "seed"
        ].__contains__(key):
            return int(value)
        elif ["ddim_eta", "scale"].__contains__(key):
            return float(value)
        return value


    def enqueue_results(self, saved_files):
        log.info("Enqueuing results")
        connection, channel = connect_queue("response_queue")
        publish_queue(channel, json.dumps(saved_files), "response_queue")
        disconnect_queue(connection, "response_queue")


    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        log.info(" [x] Received request")

        # Run stable diffusion
        log.info(" Running stable diffusion sample...")
        options = SCRIPTS["txt2img"]

        for k,v in data.items():
            n = 0
            for opt in options:
                if opt[0] == k:
                    options[n] = (opt[0], self.process_data_value(k, v))
                n+=1

        script_type = data.get("type", "txt2img")
        if script_type == "txt2img":
            saved_files = self.txt2img_loader.sample(options=options)
        else:
            saved_files = self.img2img_loader.sample(options=options)

        # enqueue result in a separate queue
        self.enqueue_results(saved_files)

        log.info("Completed")

    def __init__(self):
        try:
            connection, channel = connect_queue("request_queue")
            start_consumer(channel, self.callback, "request_queue")
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

if __name__ == "__main__":
    Receiver()