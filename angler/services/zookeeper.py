import json

from kazoo.client import KazooClient
from kazoo.recipe.watchers import ChildrenWatch, DataWatch

from angler.service import IService


class Zookeeper(IService):
    def __init__(self, name, base_path, hosts):
        IService.__init__(self, name)
        self.base_path = base_path
        self.zk = KazooClient(hosts)

    def start(self, angler):
        self.zk.start()

    def stop(self):
        self.zk.stop()

    def get(self, path):
        node = self.zk.get(self.base_path + path)
        return json.loads(node[0].decode('utf-8'))

    def set(self, path, value):
        self.zk.ensure_path(path)
        self.zk.set(path, value)

    def delete(self, path):
        self.zk.delete(path)

    def get_children(self, path):
        result = []
        for node in self.zk.get_children(self.base_path + path):
            result.append(node)
        return result

    def watch_children(self, path, callback):
        ChildrenWatch(self.zk, self.base_path + path, callback)

    def watch(self, path, modify_func, remove_func):
        def watch_callback(node, stat):
            if stat is None:  # 删除
                remove_func()
                return False
            else:
                result = node.decode('utf-8')
                try:
                    result = json.loads(result)
                except:
                    pass
                modify_func(result)
        DataWatch(self.zk, self.base_path + path, watch_callback)


def factory(name, conf):
    return Zookeeper(
        name,
        conf['base_path'],
        conf['hosts'],
    )
