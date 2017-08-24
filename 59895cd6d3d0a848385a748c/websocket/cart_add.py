def invoke(services, packet, response):
    services['mongo']['cart'].find_one({
        'loginid': packet['data']['loginid'],
        'password': packet['data']['password']
    })
