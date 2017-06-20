import json


def factory(params):
    service = params.get('service')
    if service is None:
        service = 'zookeeper'

    def invoke(services, packet, response):
        zookeeper = services[service]
        path = packet['data']['path']
        value = packet['data']['value']
        zookeeper.set(path, json.dumps(value))
        response.send({
            'event': '{0}._set'.format(service),
            'data': {
                path: path,
                value: value,
            },
            'remote': True
        })
    return {
        'result': ['{0}._get'.format(service)],
        'invoke': invoke
    }
