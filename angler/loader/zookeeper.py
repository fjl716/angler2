from angler.container import Container
from angler.event import event_factory
from angler.loader import ILoader
from angler.protocols import protocol_factory
from angler.service import service_factory
from angler.services.zookeeper import Zookeeper
from angler.sources import source_factory


class ZKLoader(ILoader):
    def __init__(self):
        self.zookeeper = None

    def start(self, angler):

        self.zookeeper = Zookeeper('master_zookeeper', '/angler/{0}/'.format(angler_id), zk_hosts)
        self.zookeeper.start(self)
        services = angler.services
        containers = angler.containers
        
        def modify_service(name):
            print(name)
            self.name = name

        def remove_service():
            pass

        self.zookeeper.watch('', modify_service, remove_service)

        # 初始化services
        def init_services(service_names):
            for service_name in service_names:

                def modify_service(service_conf):
                    service = services.get(service_name)
                    if service is not None:
                        service.stop()
                        del services[service_name]
                    service = service_factory(service_conf['package'], service_name, service_conf)
                    if service is None:
                        return
                    services[service_name] = service
                    services[service_name].start(self)
                    self.logger.info('add service {0}'.format(service_name))

                def remove_service():
                    services[service_name].stop()
                    del services[service_name]
                    self.logger.info('delete service {0}'.format(service_name))

                if service_name not in services.keys():    # 插入新增服务
                    self.zookeeper.watch(
                        'services/{0}'.format(service_name),
                        modify_service,
                        remove_service
                    )
        self.zookeeper.watch_children('services', init_services)

        # 初始化containers
        def init_containers(container_names):
            for container_name in container_names:
                def modify_container(container_conf):
                    old = containers.get(container_name)
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
                    containers[container_name] = container

                    # 初始化events
                    def init_events(event_names):
                        for event_name in event_names:
                            if container.events.get(event_name) is None:
                                def modify_event(event_conf):
                                    event = event_factory(event_conf)
                                    container.events[event_name] = event
                                    angler.logger.logger.info('event {0} -> {1}'.format(event.event, event.result))

                                def remove_event():
                                    del container.events[event_name]

                                self.zookeeper.watch(
                                    'containers/{0}/events/{1}'.format(container.name, event_name),
                                    modify_event,
                                    remove_event
                                )

                    self.zookeeper.watch_children('containers/{0}/events'.format(container.name), init_events)
                    containers[container_name].start(self)

                def remove_container(name):
                    services[name].stop()
                    del services[name]
                if container_name not in services.keys():    # 插入新增容器
                    self.zookeeper.watch(
                        'containers/{0}'.format(container_name),
                        modify_container,
                        remove_container,
                    )

        self.zookeeper.watch_children('containers', init_containers)

    def stop(self):
        pass

    def load(self, angler):
        pass


def factory(conf):
    return ZKLoader()
