from abc import ABCMeta, abstractmethod
from random import random


class AChannel(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.id = str(random())[2:]
        self.source = None

    def arrive(self, data):
        self.source.arrive(self, data)

    @abstractmethod
    def send(self, data):
        pass

    @abstractmethod
    def close(self):
        pass
