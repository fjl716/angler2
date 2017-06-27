def factory(collection, service='mongo'):
    def invoke(services, packet, response):
        mongo = services[service]
        result = mongo[collection].findone(packet['data'])
        response.send({
            'data': result,
            'remote': True
        })
    return {
        'event': '{0}.findone'.format(collection),
        'result': ['{0}._findone'.format(collection)],
        'invoke': invoke
    }
