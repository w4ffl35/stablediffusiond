#!/usr/bin/env python
"""
A consumer which watches a queue and sends messages over a socket to a client.
"""

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

    soc = None
    soc_connection = None
    soc_addr = None

    def __init__(self):
        self.host = "localhost"  # the host this service is running on
        self.port = 50007  # the port to listen on
        self.max_client_connections = 1  # the maximum number of clients to accept
        self.run()
        #threading.Thread(target=self.connect_to_queue, args=("response_queue",)).start()
        self.connect_to_queue("response_queue")
        # self.open_socket()
        # self.connect_to_queue("response_queue")

    def run(self):
        """
        Starts a new thread with a client that has a connection to stablediffusion_responsed
        :return: None
        """
        self.thread = threading.Thread(target=self.connect_server)
        self.thread.start()

    def connect_server(self):
        """
        Connect to stablediffusion_responsed socket and listen for responses.
        :return: None
        """
        self.open_socket()
        self.listen_for_connections()

    def open_socket(self):
        """
        Open a socket to listen for incoming connections.
        :return: None
        """
        log.info(f"Connecting stablediffusiond to host {self.host} on port {self.port}")
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.soc.bind((self.host, self.port))
        except socket.error as err:
            log.error(f"Failed to open a socket at {self.host}:{self.port}")
            log.error(str(err))
        log.info(f"Socket opened {self.soc}")

    def listen_for_connections(self):
        """
        Listen for incoming connections.
        Returns:
        """
        while True:
            self.soc.listen(self.max_client_connections)
            self.soc_connection, self.soc_addr = self.soc.accept()
            log.info(f"Connection established with {self.soc_addr}")

    def connect_to_queue(self, queue_name):
        """
        Connect to a queue and start listening for messages.
        :return: None
        """
        try:
            _connection, channel = connect_queue(queue_name)
            start_consumer(channel, self.queue_listener, queue_name)
        except KeyboardInterrupt:
            log.warning("Interrupted")
            sys.exit(0)

    def queue_listener(self, _channel, _method, _properties, body):
        """
        Handle messages from the queue.
        :param _channel: channel
        :param _method: method
        :param _properties: properties
        :param body: body
        :return: None
        """
        log.info(" [x] Received response")
        saved_files = json.loads(body)

        # send results to connected soc client
        self.soc_connection.sendall(json.dumps(saved_files).encode("utf-8"))

        log.info("Completed")


if __name__ == "__main__":
    # Start the response handler.
    ResponseHandler()
