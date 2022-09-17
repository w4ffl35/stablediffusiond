#!/usr/bin/env python
"""
Send a message to the queue. Called from bin/client.sh or can be called directly.
"""
import sys
from connect import connect_queue, disconnect_queue, publish_queue


def send(message):
    """
    Send a message to the queue.
    :param data: a dictionary with the data to send
    :return: None
    """
    print("SEND")
    print(message)
    connection, channel = connect_queue("request_queue")
    publish_queue(channel, message, "request_queue")
    disconnect_queue(connection, "request_queue")


if __name__ == '__main__':
    # get data json from command line argument
    print(sys.argv[1])
    send(sys.argv[1])
