def factory(collection, service='mongo'):
    def invoke(services, packet, response):
        mongo = services[service]
        result = mongo[collection].findsimple(packet['data'])
        response.send({
            'data': result,
            'remote': True
        })
    return {
        'event': '{0}.findsimple'.format(collection),
        'result': ['{0}._findsimple'.format(collection)],
        'invoke': invoke
    }
