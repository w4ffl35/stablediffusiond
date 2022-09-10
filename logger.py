import logging as log
import json
from datetime import datetime


def logging():
    obj = log.getLogger()
    log.basicConfig(level=log.INFO)
    return obj


def format_message(msg):
    # add date time to message
    return f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg}"


def info(msg):
    logging().info(f"{format_message(msg)}")


def warning(msg):
    logging().warning(f"{format_message(msg)}")


def error(msg):
    logging().error(f"{format_message(msg)}")
