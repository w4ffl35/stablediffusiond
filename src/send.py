#!/usr/bin/env python
"""
Send a message to the queue. Called from bin/client.sh or can be called directly.
"""
import sys
from settings import SERVER


def send(message):
    """
    Send a message to the queue.
    :param data: a dictionary with the data to send
    :return: None
    """
    connection, channel = SERVER["request_queue"]["connect"].connect_queue("request_queue")
    SERVER["request_queue"]["connect"].publish_queue(channel, message, "request_queue")
    SERVER["request_queue"]["connect"].disconnect_queue(connection, "request_queue")


if __name__ == '__main__':
    # get data json from command line argument
    print(sys.argv[1])
    send(sys.argv[1])
