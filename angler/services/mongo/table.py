from pymongo.collection import Collection

from angler.services.mongo import MongoDatabase


class MongoTable(object):
    def __init__(self, name, init, simple_fields):
        self.database: MongoDatabase = None
        self.name = name
        self.init = init
        self.simple_fields = simple_fields
        self.collection: Collection = None

    def simple(self, doc):
        result = {}
        for field in self.simple_fields:
            result[field] = doc.get(field)
        return result

    def delete(self, query):
        self.collection.delete_one(query)

    def find(self, query: dict, skip=0, limit=999):
        self.collection.find(query).skip(skip).limit(limit)
        result = []
        for item in self.collection.find(query):
            result.append(item)
        return result

    def find_one(self, query: dict):
        return self.collection.find_one(
            query
        )

    def find_simple(self, query: dict):
        result = self.collection.find_one(
            query
        )
        if result is None:
            return result
        return self.simple(result)

    def find_simples(self, query: dict):
        result = []
        for item in self.find(query):
            result.append(self.simple(item))
        return result

    def update(self, query: dict):
        pass

    def insert(self, doc):
        for field in self.simple_fields:
            name = field[0]
            invoke = field[1]
            if name not in doc:
                doc[name] = invoke()
        self.collection.insert_one(
            doc
        )
        return doc

    def size(self, query: dict):
        return self.collection.find(query).count()


