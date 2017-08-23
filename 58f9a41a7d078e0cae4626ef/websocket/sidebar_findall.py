def invoke(services, packet, response):
    data = services['mongo']['sidebar'].find({})
    roots = list(filter(lambda sidebar: sidebar.get('parent') is None, data))
    for item in roots:
        item['items'] = list(filter(lambda sidebar: sidebar.get('parent') == item['_id'], data))
    response.send({
        'data': roots,
        'remote': True
    })
