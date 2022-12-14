"""
Collection of functions to connect to the queue and publish messages.
"""

try:
    import pika
except ImportError:
    print("Unable to import pika. Please install requirements.")
    pika = None
try:
    from stablediffusiond.settings import SERVER
except ImportError:
    print("Unable to import settings file. Please create a settings.py file.")
    SERVER = {}
from logger import info, error


def params(queue_system):
    """
    Gets the connection parameters from the settings file
    :param queue_system:
    :return: queue, host, queue_system: the queue, host and queue system name from the settings file
    """
    try:
        queue_settings = SERVER[queue_system]
        host = queue_settings["host"]
        queue = queue_settings["queue_name"]
    except KeyError:
        error(f"Unable to find settings for {queue_system} in settings file")
        return None, None, None
    return queue, host, queue_settings["name"]


def connect_queue(queue_system):
    """
    Connects to the Queue. Starts a consumer if a callback is provided.
    :param queue_system:
    :return: connection, channel: the connection and channel objects for the queue
    """
    # get connection parameters
    queue, host, queue_system = params(queue_system)

    # connect to queue
    info(f"Starting connection to {queue_system}")
    info(f"Connecting to {queue_system} host {host}...")
    if pika:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        channel = connection.channel()
        info(f"Declaring {queue_system} queue {queue}...")
        channel.queue_declare(queue=queue)
    else:
        error("Unable to connect to queue. Pika not installed.")
        return None, None

    return connection, channel


def start_consumer(channel, callback, queue_system):
    """
    Starts a consumer on the queue and uses the callback function to process messages
    :param channel:
    :param callback:
    :param queue_system:
    :return: None
    """
    # get connection parameters
    queue, _host, queue_system = params(queue_system)
    channel.basic_consume(queue=queue, auto_ack=True, on_message_callback=callback)
    info(f' [*] {queue_system} Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def publish_queue(channel, contents, queue_system):
    """
    Publishes a message to the Queue
    :param channel:
    :param contents:
    :param queue_system:
    :return:
    """
    queue, _host, _queue_system = params(queue_system)
    channel.basic_publish(exchange="", routing_key=queue, body=contents)
    print(" [x] Sent 'Hello World!'")


def disconnect_queue(connection, queue_system):
    """
    Disconnects from the Queue
    :param connection:
    :param queue_system:
    :return:
    """
    if connection is None:
        error("Tried to close connection, but nothing to close")
        return

    _queue, _host, queue_system = params(queue_system)
    info(f"Closing {queue_system} connection...")
    connection.close()
