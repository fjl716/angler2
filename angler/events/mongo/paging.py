def factory(collection, service='mongo'):
    def invoke(services, packet, response):
        mongo = services[service]
        result = mongo[collection].find(packet['data'])
        response.send({
            'event': '{0}._paging'.format(collection),
            'data': result,
            'remote': True
        })
    return {
        'result': [],
        'invoke': invoke
    }
