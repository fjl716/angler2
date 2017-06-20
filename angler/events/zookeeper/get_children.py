def factory(params):
    service = params.get('service')
    if service is None:
        service = 'zookeeper'

    def invoke(services, packet, response):
        zookeeper = services[service]
        path = packet['data']['path']
        value = zookeeper.get_children(path)
        response.send({
            'event': '{0}._get_children'.format(service),
            'data': {
                path: path,
                value: value
            },
            'remote': True
        })
    return {
        'result': ['{0}._get_children'.format(service)],
        'invoke': invoke
    }
