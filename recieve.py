#!/usr/bin/env python
import sys
import os
import json
import logger as log
from connect import connect_queue, start_consumer
from settings import SCRIPTS

# import settings and set path for script imports
from settings import GENERAL
SCRIPTS_ROOT = GENERAL["sd_scripts"]
PYTHON_PATH = GENERAL["sd_python_path"]
sys.path.append(os.path.dirname(os.path.dirname(SCRIPTS_ROOT)))
sys.path.append(os.path.dirname(os.path.join(os.path.dirname(SCRIPTS_ROOT), "..")))

from classes.txt2img import Txt2Img


loader = Txt2Img(options=SCRIPTS["txt2img"])


def callback(ch, method, properties, body):
    data = json.loads(body)
    log.info(" [x] Received request")

    # Run stable diffusion
    log.info(" Running stable difussion sample...")
    options = SCRIPTS["txt2img"]
    print(body)
    for k,v in data.items():
        n = 0
        for opt in options:
            if opt[0] == k:
                options[n] = (opt[0], v)
            n+=1
    loader.sample(options=options)
    log.info("Completed")


if __name__ == '__main__':
    try:
        connection, channel = connect_queue()
        start_consumer(channel, callback)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
