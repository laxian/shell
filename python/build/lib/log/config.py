import json


class Config(object):
    def __init__(self, config_path):
        self.config_path = config_path
        with open(config_path, "r") as config_file:
            self.config = json.loads(config_file.read())

    @staticmethod
    def parse(self, config_path):
        return Config(config_path)

    def config(self):
        return self.config
