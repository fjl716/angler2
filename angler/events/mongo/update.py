def factory(collection, service='mongo'):
    def invoke(services, packet, response):
        mongo = services[service]
        data = packet['data']
        if 'query' in data:
            query = data['query']
            data_set = {'$set': data['set']}
        else:
            query = {
                '_id': data['_id']
            }
            data_set = data
            del data_set['_id']
        result = mongo[collection].update(query, data_set)
        response.send({
            'data': result,
            'remote': True
        })
    return {
        'event': '{0}.update'.format(collection),
        'result': ['{0}._update'.format(collection)],
        'invoke': invoke
    }
