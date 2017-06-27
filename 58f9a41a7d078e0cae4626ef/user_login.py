def invoke(services, packet, response):
    user = services['mongo']['user'].find_one({
        'loginid': packet.get('loginid'),
        'password': packet.get('password')
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
