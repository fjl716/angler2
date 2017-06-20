from abc import ABCMeta, abstractmethod
from random import random


class Equipment(object):
    __metaclass__ = ABCMeta

    def __init__(self, container):
        self.id = str(random())[2:]
        self.container = container

    def send(self, packet):
        pass

    @abstractmethod
    def arrive(self, packet):
        pass

