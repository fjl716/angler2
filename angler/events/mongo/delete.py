def factory(collection, service='mongo'):
    def invoke(services, packet, response):
        mongo = services[service]
        result = mongo[collection].delete(packet['data'])
        response.send({
            'data': result,
            'remote': True
        })
    return {
        'event': '{0}.delete'.format(collection),
        'result': ['{0}._delete'.format(collection)],
        'invoke': invoke
    }
