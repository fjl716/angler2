from angler.service import IService


class Cache(IService):
    def __init__(self):
        IService.__init__(self, 'cache')
        self.angler = None

    def stop(self):
        pass

    def start(self, angler):
        self.angler = angler

    def get(self, key, default=None):
        return self.angler.zookeeper.get('cache/{0}'.format(key))

    def set(self, key, value, ttl=None):
        self.angler.zookeeper.set('cache/{0}'.format(key), value)

    def delete(self, key):
        self.angler.zookeeper.delete('cache/{0}'.format(key))


def factory(name, conf):
    print(name)
    return Cache()
