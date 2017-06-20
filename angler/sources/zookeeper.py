from angler.source import ASource
from kazoo.client import KazooClient


class ZookeeperSource(ASource):
    def __init__(self, protocol, hosts):
        ASource.__init__(self, protocol)
        self.hosts = hosts

    def start(self, container):
        ASource.start(self, container)
        zk = KazooClient(self.hosts)
        zk.start()

    def get_name(self):
        pass

    def stop(self):
        pass


def create_zookeeper(protocol, conf):
    return ZookeeperSource(protocol, conf['hosts'])

