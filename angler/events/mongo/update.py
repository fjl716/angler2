def factory(collection, service='mongo'):
    def invoke(services, packet, response):
        mongo = services[service]
        result = mongo[collection].update(packet['data'])
        response.send({
            'data': result,
            'remote': True
        })
    return {
        'event': '{0}.update'.format(collection),
        'result': ['{0}._update'.format(collection)],
        'invoke': invoke
    }
