from angler.services.mongo.database import MongoDatabase


def factory(name, conf):
    return MongoDatabase(
        name,
        conf['host'],
        conf['port'],
        conf['database']
    )
