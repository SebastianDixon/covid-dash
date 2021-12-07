import json
import os
import logging

"""
This module initialises the environment variables and is run before any other modules
"""

CONFIG_PATH = "config.json"


def load_env():
    with open(CONFIG_PATH, "r") as config_file:
        configs = json.load(config_file)

        for key, val in configs.items():
            os.environ[key.upper()] = val


def setup_logging():
    logging.basicConfig(
        filename=os.environ["SERVER_LOG_PATH"],
        level=logging.DEBUG,
    )


def setup_server():
    load_env()
    setup_logging()


setup_server()


import website

website.app.run()
