import pika
import json
from logger import info, error

with open('stablediffusiond_settings.json') as f:
    settings = json.load(f)


def params():
    """
    Gets the connection parameters from the settings file
    :return: queue, host, queue_system: the queue, host and queue system name from the settings file
    """
    server_settings = settings["server"]
    queue_system = server_settings["queue_system"]
    queue_settings = settings["server"][queue_system]
    host = queue_settings["host"]
    queue = queue_settings["queue_name"]
    return queue, host, queue_system


def connect_queue():
    """
    Connects to the Queue and starts a consumer if a callback is provided, otherwise it just connects
    :return: connection, channel: the connection and channel objects for the queue
    """
    # get connection parameters
    queue, host, queue_system = params()

    # connect to queue
    info(f"Starting connection to {queue_system}")
    info(f"Connecting to {queue_system} host {host}...")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()

    info(f"Declaring {queue_system} queue {queue}...")
    channel.queue_declare(queue=queue)

    return connection, channel

def start_consumer(channel, callback):
    """
    Starts a consumer on the queue and uses the callback function to process messages
    :param channel:
    :param callback:
    :return: None
    """
    # get connection parameters
    queue, _host, queue_system = params()
    channel.basic_consume(queue=queue, auto_ack=True, on_message_callback=callback)
    info(f' [*] {queue_system} Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def publish_queue(channel, contents):
    """
    Publishes a message to the Queue
    :param channel:
    :param contents:
    :return:
    """
    queue, _host, _queue_system = params()
    channel.basic_publish(exchange="", routing_key=queue, body=contents)
    print(" [x] Sent 'Hello World!'")


def disconnect_queue(connection):
    """
    Disconnects from the Queue
    :param connection:
    :return:
    """
    if connection is None:
        error("Tried to close connection, but nothing to close")
        return

    queue, _host, queue_system = params()
    info(f"Closing {queue_system} connection...")
    connection.close()