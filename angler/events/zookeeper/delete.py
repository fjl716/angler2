def factory(params):
    service = params.get('service')
    if service is None:
        service = 'zookeeper'

    def invoke(services, packet, response):
        zookeeper = services[service]
        path = packet['data']['path']
        zookeeper.delete(path)
        response.send({
            'event': '{0}._delete'.format(service),
            'data': {
                path: path,
            },
            'remote': True
        })
    return {
        'result': ['{0}._delete'.format(service)],
        'invoke': invoke
    }
