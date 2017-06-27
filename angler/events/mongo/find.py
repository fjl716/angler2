def factory(collection, service='mongo'):
    def invoke(services, packet, response):
        mongo = services[service]
        result = mongo[collection].find(packet['data'])
        response.send({
            'data': result,
            'remote': True
        })
    return {
        'event': '{0}.find'.format(collection),
        'result': ['{0}._find'.format(collection)],
        'invoke': invoke
    }
