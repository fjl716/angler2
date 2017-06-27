def factory(collection, service='mongo'):
    def invoke(services, packet, response):
        mongo = services[service]
        result = mongo[collection].find(packet.get('data'))
        response.send({
            'data': result,
            'remote': True
        })
    return {
        'event': '{0}.findall'.format(collection),
        'result': ['{0}._findall'.format(collection)],
        'invoke': invoke
    }
