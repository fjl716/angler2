def invoke(services, packet, response):
    data = services['mongo']['sidebar'].find({})
    roots = list(filter(lambda sidebar: sidebar.get('parent') is None, data))
    for item in roots:
        item['items'] = list(filter(lambda sidebar: sidebar.get('parent') == item['_id'], data))
    response.send({
        'data': roots,
        'remote': True
    })
    # roots = data.filter(item= > item.parent == = undefined)
    # roots.map(root= > {
    #     root.items = list.filter(child= > {
    # return child.parent + '' === root._id + ''
    # });
    # // console.log(item._id);
    # });
    # print(data)
    # if user is None:
    #     response.send({
    #         'error': 1,
    #         'remote': True
    #     })
    # else:
    #     del user['password']
    #     response.send({
    #         'data': user,
    #         'remote': True
    #     })
