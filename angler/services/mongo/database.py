from pymongo import MongoClient

from angler.service import IService


class MongoDatabase(IService):
    def start(self, angler):
        pass

    def stop(self):
        pass

    def __init__(self, name: str, host: str, port: int, database: str):
        IService.__init__(self, name)
        client = MongoClient(host, port)
        self.db = client.get_database(database)
        self.tables = {}

    def __getitem__(self, key):
        return self.tables[key]

    def __setitem__(self, key, table):
        self.tables[table.name] = table
        table.database = self
        table.collection = self.db.get_collection(table.name)

    def find(self, name, query):
        self.db.get_collection(name).find(query)
