import json
import queue as q
import threading
import socket
import logger as log
from settings import SCRIPTS, SERVER
from classes.txt2img import Txt2Img
from classes.img2img import Img2Img

class Simple:
    soc = None
    soc_connection = None
    soc_addr = None
    request_queue = None
    response_queue = None
    thread = None
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

    @staticmethod
    def process_data_value(key, value):
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

    @staticmethod
    def decode_binary_string(message):
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

    def __init__(self):
        self.outgoing_socket = None
        self.incoming_socket = None
        self.connected_to_client = False
        # self._txt2img_loader = Txt2Img(
        #     options=SCRIPTS["txt2img"],
        #     model=self.model,
        #     device=self.device
        # )
        self._img2img_loader = Img2Img(
            options=SCRIPTS["img2img"],
            model=None,
            device=None
            # model=self._txt2img_loader.model,
            # device=self._txt2img_loader.device
        )
        self.request_queue = q.Queue()
        self.response_queue = q.Queue()
        self.host = "localhost"  # the host this service is running on
        self.port = 50007  # the port to listen on
        self.max_client_connections = 1  # the maximum number of clients to accept
        self.run()

    def run(self):
        """
        Starts a new thread which opens a socket and waits for connections from
        a client.
        :return: None
        """

        # messages out to client
        # self.open_incoming_socket()
        # self.incoming_thread = threading.Thread(target=self.listen_for_connection_from_client)
        # self.incoming_thread.start()
        # threading.Thread(target=self.response_queue_worker).start()

        # messages in from client
        self.connect_outgoing_socket()
        threading.Thread(target=self.receive_message_from_server).start()
        threading.Thread(target=self.request_queue_worker).start()

    def open_incoming_socket(self):
        """
        Open a socket to listen for incoming connections.
        :return: None
        """
        log.info(f"Opening a socket for incoming connections localhost on port 50006")
        self.incoming_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.incoming_socket.bind(("localhost", 50006))
        except socket.error as err:
            log.error(f"Failed to open a socket at {self.host}:{self.port}")
            log.error(str(err))
            return
        log.info(f"Socket opened {self.incoming_socket}")

    def listen_for_connection_from_client(self):
        """
        Listen for incoming connections from client and pushes messages to them.
        Returns:
        """
        while True:
            self.incoming_socket.listen(self.max_client_connections)
            self.incoming_connection, self.incoming_sock_address = self.incoming_socket.accept()

            log.info(f"Connection established with {self.incoming_sock_address}")

    def connect_outgoing_socket(self):
        self.outgoing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.outgoing_socket.connect(("localhost", 50007))

    def receive_message_from_server(self):
        while True:
            message = self.outgoing_socket.recv(1024)
            log.info("message received")
            print(message)
            self.request_queue.put(message)

    def request_queue_worker(self):
        while True:
            # run request worker
            item = self.request_queue.get()
            print("item acquired")
            print(item)
            self.run_stable_diffusion(item)

    def response_queue_worker(self):
        while True:
            item = self.response_queue.get()
            saved_files = json.loads(item)
            print("saved files")
            # self.incoming_connection.sendall(json.dumps(saved_files).encode("utf-8"))

    # def connect_client_socket(self):
    #     """
    #     gets requests from client and adds to queue
    #     Returns:
    #
    #     """
    #     check_stream = True
    #     while check_stream:
    #         data = None
    #         try:
    #             data = self.incoming_socket.recv(1024)
    #             print("got data")
    #             self.request_queue.put(data)
    #         except Exception as e:
    #             print(e)
    #             check_stream = False

    def run_stable_diffusion(self, body):
        """
        This function is called when a message is received on the queue.
        :param body: body
        :return: None
        """
        # decode body from binary to string
        body = self.decode_binary_string(body)
        data = json.loads(body)
        print(data)

        log.info(" [x] Received request")

        log.info(" Running stable diffusion sample...")
        script_type = data.get("type", "txt2img")
        options = SCRIPTS[script_type]

        # get all keys from data
        keys = data.keys()

        for index, opt in enumerate(options):
            if opt[0] in keys:
                options[index] = (opt[0], self.process_data_value(opt[0], data.get(opt[0], opt[1])))

        # if script_type == "txt2img":
        #     saved_files = self.txt2img_loader.sample(options=options)
        # else:
        saved_files = self.img2img_loader.sample(options=options)

        self.response_queue.put(saved_files)

        log.info("Completed")


if __name__ == '__main__':
    Simple()
