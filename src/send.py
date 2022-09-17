#!/usr/bin/env python
"""
Send a message to the queue. Called from bin/client.sh or can be called directly.
"""
import sys
import connect_rabbitmq
import connect_simplequeue
from settings import SERVER
import logger as log

def send(message):
    """
    Send a message to the queue.
    :param data: a dictionary with the data to send
    :return: None
    """
    queuename = SERVER["request_queue"]["name"]
    connect = None
    if queuename == "SimpleQueue":
        connect = connect_rabbitmq
    elif queuename:
        connect = connect_simplequeue
    if not connect:
        log.error("Unable to find queue system in settings file")
        return
    connection, channel = connect.connect_queue("request_queue")
    connect.publish_queue(channel, message, "request_queue")
    connect.disconnect_queue(connection, "request_queue")


if __name__ == '__main__':
    # get data json from command line argument
    log.info("Sending message to queue")
    send(sys.argv[1])
