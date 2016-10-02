from json import dump, load
from os import mkdir
from .generator import Generator

class Loader(object):
    def __init__(self, directory='markov/'):
        self._directory = directory
        try:
            mkdir(directory)
        except FileExistsError:
            pass

    def save(self, trainer_or_compiled_data, filename):
        try:
            data = trainer_or_compiled_data.compiled
        except AttributeError:
            data = trainer_or_compiled_data
        with open(self._directory + filename, 'w') as f:
            dump(data, f)

    def load(self, filename):
        with open(self._directory + filename, 'r') as f:
            data = load(f)
        return Generator(**data)
