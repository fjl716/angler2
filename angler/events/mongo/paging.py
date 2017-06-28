def factory(collection, service='mongo'):
    def invoke(services, packet, response):
        mongo = services[service]
        result = mongo[collection].find(packet['query'])
        response.send({
            'data': result,
            'remote': True
        })
    return {
        'event': '{0}.paging'.format(collection),
        'result': ['{0}._paging'.format(collection)],
        'invoke': invoke
    }
