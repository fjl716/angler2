from abc import ABCMeta, abstractmethod


class AProtocol(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self, data):
        pass

    @abstractmethod
    def serialize(self, packet):
        pass
