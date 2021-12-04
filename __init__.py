import json
import os
from flask import Flask


CONFIG_PATH = "config.json"


def load_envs():
    with open(CONFIG_PATH, "r") as config_file:
        configs = json.load(config_file)

        for key, val in configs.items():
            os.environ[key.upper()] = val


load_envs()

import website

website.app.run()
