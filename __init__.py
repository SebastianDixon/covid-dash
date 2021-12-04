import json
import os


CONFIG_PATH = "config.json"


def load_env():
    with open(CONFIG_PATH, "r") as config_file:
        configs = json.load(config_file)

        for key, val in configs.items():
            os.environ[key.upper()] = val


load_env()

import website
website.app.run()
