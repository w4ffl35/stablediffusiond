"""
Collection of functions to connect to the queue and publish messages.
"""
import queue as q
from logger import info, error

queue = q.SimpleQueue()


def params(queue_system):
    """
    Gets the connection parameters from the settings file
    :param queue_system:
    :return: queue, host, queue_system: the queue, host and queue system name from the settings file
    """
    pass


def connect_queue(queue_system):
    """
    Connects to the Queue. Starts a consumer if a callback is provided.
    :param queue_system:
    :return: connection, channel: the connection and channel objects for the queue
    """
    return None, None



def start_consumer(channel, callback, queue_system):
    """
    Starts a consumer on the queue and uses the callback function to process messages
    :param channel:
    :param callback:
    :param queue_system:
    :return: None
    """
    # get connection parameters
    pass


def publish_queue(channel, contents, queue_system):
    """
    Publishes a message to the Queue
    :param channel:
    :param contents:
    :param queue_system:
    :return:
    """
    queue.put(contents)


def disconnect_queue(connection, queue_system):
    """
    Disconnects from the Queue
    :param connection:
    :param queue_system:
    :return:
    """
    pass
