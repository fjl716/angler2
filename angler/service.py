from abc import ABCMeta, abstractmethod


class IService(object):
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def start(self, angler):
        pass

    @abstractmethod
    def stop(self):
        pass


def service_factory(package, name, conf):
    mod = __import__(package, fromlist=[''])
    return mod.factory(name, conf)

