from abc import abstractmethod, ABCMeta

from angler.service import IService


class ILoader(IService):
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self, angler):
        pass

    @abstractmethod
    def stop(self):
        pass





