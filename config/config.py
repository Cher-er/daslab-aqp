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


@Singleton
class VAEConfig:
    def __init__(self):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "vae.json")) as f:
            config = json.load(f)
        self.config = config

    def get_config(self):
        return self.config


@Singleton
class CVAEConfig:
    def __init__(self):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "cvae.json")) as f:
            config = json.load(f)
        self.config = config

    def get_config(self):
        return self.config
