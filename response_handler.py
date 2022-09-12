#!/usr/bin/env python
import os
import sys
import json
import threading
import socket
import logger as log
from connect import connect_queue, start_consumer


class ResponseHandler:
    """
    Response handler is a second daemon which listens to the response queue
    and sends results to appropriate clients that are connected to this service.
    """

    def __init__(self):
        self.host = "localhost"  # the host this service is running on
        self.port = 50007  # the port to listen on
        self.max_client_connections = 1  # the maximum number of clients to accept
        threading.Thread(target=self.open_socket).start()
        threading.Thread(target=self.connect_to_queue, args=("response_queue",)).start()
        # self.open_socket()
        # self.connect_to_queue("response_queue")

    def open_socket(self):
        log.info(f"Connecting stablediffusiond to host {self.host} on port {self.port}")
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.soc.bind((self.host, self.port))
        except socket.error as e:
            log.error(f"Failed to open a socket at {self.host}:{self.port}")
            log.error(str(e))
            return
        log.info(f"Socket opened {self.soc}")
        self.soc.listen(self.max_client_connections)
        self.soc_connection, self.soc_addr = self.soc.accept()
        log.info(f"Connection established with {self.soc_addr}")

    def connect_to_queue(self, queue_name):
        try:
            connection, channel = connect_queue(queue_name)
            start_consumer(channel, self.queue_listener, queue_name)
        except KeyboardInterrupt:
            log.warning("Interrupted")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

    def queue_listener(self, ch, method, properties, body):
        log.info(" [x] Received response")
        saved_files = json.loads(body)

        # send results to connected soc client
        self.soc_connection.sendall(json.dumps(saved_files).encode("utf-8"))

        log.info("Completed")


if __name__ == "__main__":
    ResponseHandler()
