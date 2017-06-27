def factory(collection, service='mongo'):
    def invoke(services, packet, response):
        mongo = services[service]
        result = mongo[collection].findsimples(packet['data'])
        response.send({
            'data': result,
            'remote': True
        })
    return {
        'event': '{0}.findsimples'.format(collection),
        'result': ['{0}._findsimples'.format(collection)],
        'invoke': invoke
    }
