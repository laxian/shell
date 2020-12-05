import json


class Config(object):

    def __init__(self, config_path):
        self.config_path = config_path
        self.config = json.loads(open(config_path, 'r').read())

    @staticmethod
    def parse(self, config_path):
        return Config(config_path)

    def config(self):
        return self.config
