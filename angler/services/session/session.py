from angler.service import IService
from abc import ABCMeta, abstractmethod


class Session(IService):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set(self, link_id, name, val):
        pass

    @abstractmethod
    def remove(self, link_id, name):
        pass

    @abstractmethod
    def get(self, link_id, name):
        pass
