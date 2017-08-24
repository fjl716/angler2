import json

import sys
import os
import yaml
from kazoo.client import KazooClient


def load_yaml(file_name):
    file = open(file_name)
    result = yaml.load(file)
    file.close()
    return result


def set_value(zookeeper, path, value):
    zookeeper.ensure_path(path)
    value = bytes('{0}'.format(value), 'utf-8')
    if zookeeper.get(path)[0] != value:
        print('set {0} = {1}'.format(path, value))
        zookeeper.set(path, value)


def get_zookeeper(zookeeper, path):
    return zookeeper.get(path)[0].decode('utf-8')


def push_file(zookeeper, angler_id):
    angler_path = './{0}/'.format(angler_id)
    if not os.path.isdir(angler_path):
        # print(angler_path)
        return

    angler = load_yaml(angler_path + 'index.yaml')
    angler_zk = '/angler/{0}'.format(angler_id)
    set_value(zookeeper, angler_zk, angler['name'])

    services_zk = angler_zk + '/services'
    services_path = angler_path + 'services/'
    service = load_yaml(services_path + 'index.yaml')
    zookeeper.ensure_path(services_zk)
    for old_service in zookeeper.get_children(services_zk):
        if old_service not in service:
            zookeeper.delete('{0}/{1}'.format(services_zk, old_service))
            print('del {0}/{1}'.format(services_zk, old_service))

    for service_name in service:
        set_value(zookeeper, '{0}/{1}'.format(services_zk, service_name),
                  json.dumps(load_yaml(services_path + service_name + '.yaml')))

    for container_name in angler['containers'].keys():
        container_zk = angler_zk + '/containers/{0}'.format(container_name)
        container = angler['containers'][container_name]

        container_path = angler_path + container_name + '/'
        events = load_yaml(container_path + 'index.yaml')
        set_value(zookeeper, container_zk, json.dumps(container))

        events_zk = container_zk + '/events'
        zookeeper.ensure_path(events_zk)
        for old_event in zookeeper.get_children(events_zk):
            if old_event not in events.keys():
                zookeeper.delete('{0}/{1}'.format(events_zk, old_event))
                print('del {0}/{1}'.format(events_zk, old_event))

        for event_name in events.keys():
            event = events[event_name]
            if event.get('package') is None:
                file = open('{0}{1}.py'.format(container_path, event_name))
                event['script'] = file.read()
            set_value(zookeeper, '{0}/{1}'.format(events_zk, event_name), json.dumps(event))


def pull_file(zookeeper, angler_id):
    path = './{0}'.format(angler_id)
    if not os.path.isdir(path):
        os.mkdir(path)

    angler = dict()
    angler['id'] = angler_id
    angler_zk = '/angler/{0}'.format(angler_id)

    if not zookeeper.exists(angler_zk):
        print('not found {0} node'.format(angler_id))
        return
    angler['name'] = get_zookeeper(angler_zk)
    containers = dict()
    angler['containers'] = containers
    for container_name in zookeeper.get_children(angler_zk + '/containers'):
        containers[container_name] = json.loads(
            zookeeper.get(angler_zk + '/containers/{0}'.format(container_name))[0].decode('utf-8'))

        container = containers[container_name]

        container['events'] = dict()
        for event_name in zookeeper.get_children(angler_zk + '/containers/{0}/events/'.format(container_name)):
            event = json.loads(
                zookeeper.get(angler_zk + '/containers/{0}/events/{1}'.format(container_name, event_name))[0].decode(
                    'utf-8'))
            script = event.get('script')
            if script is not None:
                file = open('./{0}/{1}.py'.format(angler_id, event_name), 'w')
                file.write(script)
                file.close()
                del event['script']
            container['events'][event_name] = event

    services = dict()
    angler['services'] = services
    for service_name in zookeeper.get_children(angler_zk + '/services'):
        services[service_name] = json.loads(
            zookeeper.get(angler_zk + '/services/{0}'.format(service_name))[0].decode('utf-8'))

    file = open('{0}.yaml'.format(angler_id), 'w')
    yaml.dump(angler, file, default_flow_style=False)
    file.close()
    print('pull {0} finish'.format(angler_id))


def main(argv):
    if len(argv) != 3:
        return
    if argv[1] not in ['push', 'pull']:
        return

    file = open('angler_zookeeper.yaml')
    conf = yaml.load(file)
    file.close()
    zookeeper = KazooClient(conf['zookeeper']['hosts'])
    zookeeper.start()
    if argv[1] == 'push':
        push_file(zookeeper, argv[2])
    elif argv[1] == 'pull':
        pull_file(zookeeper, argv[2])


if __name__ == "__main__":
    main(sys.argv)
