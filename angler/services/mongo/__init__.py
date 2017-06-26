from angler.services.mongo.database import MongoDatabase


def factory(name, conf):
    print(conf.get('host'))
    return MongoDatabase(
        name,
        conf['host'],
        conf['port'],
        conf['database']
    )
