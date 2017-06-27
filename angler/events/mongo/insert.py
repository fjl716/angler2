def factory(collection, service='mongo'):
    def invoke(services, packet, response):
        mongo = services[service]
        result = mongo[collection].insert(packet['data'])
        response.send({
            'data': result,
            'remote': True
        })
    return {
        'event': '{0}.insert'.format(collection),
        'result': ['{0}._insert'.format(collection)],
        'invoke': invoke
    }
