"""
Wrapper functions for logging
"""
import os
import logging as log
from datetime import datetime


def logging():
    """
    Crates and returns a logger object
    Returns:

    """
    obj = log.getLogger()
    log.basicConfig(level=log.INFO)
    path = os.path.dirname(os.path.realpath(__file__))
    log_file = log.FileHandler(f"{path}/../log/stablediffusiond.log")
    log_file.setLevel(log.INFO)
    log_file.setFormatter(log.Formatter("%(asctime)s %(levelname)s %(message)s"))
    obj.addHandler(log_file)
    return obj


def format_message(msg):
    """
    Adds timestamp to log message.
    :param msg: Message to be logged
    :return: Formatted message
    """
    return f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg}"


def info(msg):
    """
    Log formatted info message.
    :param msg: Message to be logged
    :return: None
    """
    logging().info(format_message(msg))


def warning(msg):
    """
    Log formatted warning message.
    :param msg: Message to be logged
    :return: None
    """
    logging().warning(format_message(msg))


def error(msg):
    """
    Log formatted error message.
    :param msg: Message to be logged
    :return: None
    """
    logging().error(format_message(msg))
