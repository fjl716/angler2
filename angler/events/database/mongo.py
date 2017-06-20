from functools import partial

from angler.container import Container


def mongo_delete(services, request, response, collection):
    response.send(
        services.mongo[collection].delete(request.packet),
        True
    )


def mongo_find(services, request, response, collection):
    response.send(
        services.mongo[collection].find(request.packet),
        True
    )


def mongo_find_all(services, request, response, collection):
    response.send(
        services.mongo[collection].find({}),
        True
    )


def mongo_find_one(services, request, response, collection):
    response.send(
        services.mongo[collection].find_one(request.packet),
        True
    )


def mongo_find_simple(services, request, response, collection):
    response.send(
        services.mongo[collection].find_simple(request.packet),
        True
    )


def mongo_find_simples(services, request, response, collection):
    response.send(
        services.mongo[collection].find_simples(request.packet['data']['query']),
        True
    )


def mongo_insert(services, request, response, collection):
    response.send(
        services.mongo[collection].insert(request.packet),
        True
    )


def mongo_paging(services, request, response, collection):
    data = request.packet['data']
    query = data.get('query')
    page_size = data['pageSize']
    current_page = data['currentPage']
    response.send({
        'items': services.mongo[collection].find(
            query,
            page_size,
            (current_page - 1) * page_size
        ),
        'total': services.mongo[collection].size(query),
        'pageSize': page_size,
        'currentPage': current_page,
        },
        True
    )


def mongo_update(services, request, response, collection):

    response.send(
        services.mongo[collection].update(request.packet),
        True
    )


def mongo_link_delete(services, request, response, collection):
    pass


def mongo_link_update(services, request, response, collection):
    pass


def event_mongo(container: Container, collection: str, event: str, work: str, invoke):
    if event is None:
        event = '{0}.{1}'.format(collection, work)
    container.add_event(
        event,
        ['{0}._{1}'.format(collection, work)],
        partial(invoke, collection=collection)
    )

event_mongo_delete = partial(event_mongo, work='delete', invoke=mongo_delete)
event_mongo_find = partial(event_mongo, work='find', invoke=mongo_find)
event_mongo_findall = partial(event_mongo, work='findall', invoke=mongo_find_all)
event_mongo_find_one = partial(event_mongo, work='findone', invoke=mongo_find_one)
event_mongo_find_simple = partial(event_mongo, work='findsimple', invoke=mongo_find_simple)
event_mongo_find_simples = partial(event_mongo, work='findsimples', invoke=mongo_find_simples)
event_mongo_insert = partial(event_mongo, work='insert', invoke=mongo_insert)
event_mongo_paging = partial(event_mongo, work='paging', invoke=mongo_paging)
event_mongo_update = partial(event_mongo, work='update', invoke=mongo_update)


def event_mongo_all(container: Container, collection: str):
    event_mongo_delete(container, collection, None)
    event_mongo_delete(container, collection, None)
    event_mongo_find(container, collection, None)
    event_mongo_findall(container, collection, None)
    event_mongo_find_one(container, collection, None)
    event_mongo_find_simple(container, collection, None)
    event_mongo_find_simples(container, collection, None)
    event_mongo_insert(container, collection, None)
    event_mongo_paging(container, collection, None)
    event_mongo_update(container, collection, None)

