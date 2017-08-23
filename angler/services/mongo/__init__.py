from angler.services.mongo.database import MongoDatabase
from angler.services.mongo.table import MongoTable


def factory(name, conf):
    mongo = MongoDatabase(
        name,
        conf['host'],
        conf['port'],
        conf['database']
    )
    for item in conf['collections'].items():
        name = item[0]
        init = {}
        simple = []
        if item[1] is not None:
            init = item[1].get('init', init)
            simple = item[1].get('simple', simple)
        mongo[name] = MongoTable(name, init, simple)
    return mongo
