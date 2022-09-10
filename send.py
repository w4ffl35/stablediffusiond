#!/usr/bin/env python
import sys
from connect import connect_queue, disconnect_queue, publish_queue
import json


def send(data):
    connection, channel = connect_queue()
    publish_queue(channel, json.dumps(data))
    disconnect_queue(connection)


if __name__ == '__main__':
    # get data json from command line argument
    data = json.loads(sys.argv[1])
    send(data)