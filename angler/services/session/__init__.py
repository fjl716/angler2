from angler.services.session.mongo_session import MongoSession


def factory(name, conf):
    session = None
    if conf['session_type'] == 'mongo':
        session = MongoSession(
            name,
            conf['host'],
            conf['port'],
            conf['database']
        )
    return session
