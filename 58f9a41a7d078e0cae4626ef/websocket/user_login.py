def invoke(services, packet, response):
    user = services['mongo']['user'].find_one({
        'loginid': packet['data']['loginid'],
        'password': packet['data']['password']
    })
    if user is None:
        response.send({
            'error': 1,
            'remote': True
        })
    else:
        del user['password']
        response.send({
            'data': user,
            'remote': True
        })
