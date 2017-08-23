from pymongo import MongoClient
from angler.service import IService
from angler.services.session.session import Session


class MongoSession(Session):
    def __init__(self, name: str, host: str, port: int, database: str):
        IService.__init__(self, name)
        client = MongoClient(host, port)
        self.db = client.get_database(database)
        self.database = database
        self.collection = self.db.get_collection('session')

    def set(self, link_id, name, val):
        obj = self.collection.find_one({
            '_id': link_id
        })
        if obj is None:
            self.collection.update_one({
                '_id': link_id
            }, {
                '$set': {name: val}
            })
        else:
            self.collection.insert({
                '_id': link_id,
                name: val
            })

    def remove(self, link_id, name):
        pass

    def get(self, link_id, name):
        obj = self.collection.find_one({
            '_id': link_id
        })
        if obj is None:
            return None
        return obj[name]

    def stop(self):
        pass

    def start(self, angler):
        pass


