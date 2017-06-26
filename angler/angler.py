from tornado import ioloop
import logging
from angler.container import Container
from angler.event import event_factory
from angler.protocols import protocol_factory
from angler.service import service_factory
from angler.services.zookeeper import Zookeeper
from angler.sources import source_factory


class Angler(object):
    def __init__(self, angler_id: str, zk_hosts):
        self.zookeeper = Zookeeper('master_zookeeper', '/angler/{0}/'.format(angler_id), zk_hosts)
        self.angler_id = angler_id
        self.name = angler_id
        self.containers = dict()
        self.services = dict()
        self.logger = logging.getLogger('Angler[{0}]'.format(angler_id))
        self.running = False

    def send(self, equipment: str, packet: dict):
        sp = self.zookeeper.get('equipments/{0}'.format(equipment))[0].split(':')
        container = self.containers.get(sp[0])
        if container is None:
            pass
        else:
            container.source.send(sp[1], packet)

    def start(self):
        self.logger.info('zookeeper start')
        self.zookeeper.start(self)

        def modify_service(name):
            self.name = name

        def remove_service():
            pass

        self.zookeeper.watch('', modify_service, remove_service)

        # 初始化services
        def init_services(service_names):
            for service_name in service_names:

                def modify_service(service_conf):
                    service = self.services.get(service_name)
                    if service is not None:
                        service.stop()
                        del self.services[service_name]
                    service = service_factory(service_conf['package'], service_name, service_conf)
                    if service is None:
                        return
                    self.services[service_name] = service
                    if self.running:
                        self.services[service_name].start(self)
                    self.logger.info('add service {0}'.format(service_name))

                def remove_service():
                    self.services[service_name].stop()
                    del self.services[service_name]
                    logging.info('delete service {0}'.format(service_name))

                if service_name not in self.services.keys():    # 插入新增服务
                    self.zookeeper.watch(
                        'services/{0}'.format(service_name),
                        modify_service,
                        remove_service
                    )
        self.zookeeper.watch_children('services', init_services)

        self.running = True
        for service in self.services.values():
            service.start(self)

        # 初始化containers
        def init_containers(container_names):
            for container_name in container_names:
                def modify_container(container_conf):
                    old = self.containers.get(container_name)
                    if old is not None:
                        old.stop()
                    protocol = protocol_factory(container_conf['protocol'])
                    if protocol is None:
                        return
                    source = source_factory(container_conf['source'], protocol)
                    if source is None:
                        return
                    container = Container(container_name, source)
                    source.container = container
                    self.containers[container_name] = container

                    # 初始化events
                    def init_events(event_names):
                        for event_name in event_names:
                            if container.events.get(event_name) is None:
                                def modify_event(event_conf):
                                    container.events[event_name] = event_factory(event_conf)

                                def remove_event():
                                    del container.events[event_name]

                                self.zookeeper.watch(
                                    'containers/{0}/events/{1}'.format(container.name, event_name),
                                    modify_event,
                                    remove_event
                                )

                    self.zookeeper.watch_children('containers/{0}/events'.format(container.name), init_events)
                    self.containers[container_name].start(self)

                def remove_container(name):
                    self.services[name].stop()
                    del self.services[name]
                if container_name not in self.services.keys():    # 插入新增容器
                    self.zookeeper.watch(
                        'containers/{0}'.format(container_name),
                        modify_container,
                        remove_container,
                    )

        self.zookeeper.watch_children('containers', init_containers)

        ioloop.IOLoop.instance().start()

    def stop(self):
        for service in self.services.values():
            service.stop(self)
        for container in self.containers.values():
            container.stop()
        self.zookeeper.stop()
