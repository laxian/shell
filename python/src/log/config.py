# -*- encoding: utf-8 -*-

import json
import os


class Config(object):
    def __init__(self, config_path):
        self.config_path = config_path
        here = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(here, config_path), "r") as config_file:
            self.config = json.loads(config_file.read())
            if 'log_dir' in self.config:
                raw_path = self.config['log_dir']
                self.config['log_dir'] = os.path.expanduser(raw_path)

    @staticmethod
    def parse(self, config_path):
        return Config(config_path)

    def config(self):
        return self.config

    @staticmethod
    def dump(config):
        here = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(here, 'config.json'), 'w') as fp:
            fp.write(json.dumps(config))
