import json
import os


class Singleton:
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


class Config:
    def __init__(self, cfg_file):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), cfg_file)) as f:
            config = json.load(f)
        self.config = config

    def get_config(self):
        return self.config


@Singleton
class VAEConfig(Config):
    def __init__(self):
        super(VAEConfig, self).__init__("vae.json")


@Singleton
class CVAEConfig(Config):
    def __init__(self):
        super(CVAEConfig, self).__init__("cvae.json")
