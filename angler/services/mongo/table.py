from pymongo.collection import Collection
import re
import time;
from angler.services.mongo import MongoDatabase
from bson import ObjectId


def json_bson(obj):
    for name in obj:
        value = obj[name]
    if type(value) == str:
        if re.match(r'^[0-9 a-f]{24}$', value) is not None:
            obj[name] = ObjectId(value)
        elif re.match(r'^D:([0-9]*)$', value) is not None:
            obj[name] = time.time()
        elif value[0] == '/':
            obj[name] = re(value.substring(1))
        else:
            pass
    elif isinstance(value, list):
        for index in range(len(value)):
            tmp = value[index]
            if isinstance(tmp, dict):
                value[index] = json_bson(tmp)
            elif re.match(r'^[0-9 a-f]{24}$', tmp):
                value[index] = ObjectId(value)
    elif isinstance(value, dict):
        json_bson(value)
    return obj


class MongoTable(object):
    def __init__(self, name, init, simple_fields):
        self.database: MongoDatabase = None
        self.name = name
        self.init = {}

        def new_id():
            return ObjectId()

        for field in init:
            value = init[field]
            if value == 'new_id()':
                self.init[field] = new_id
            else:
                def default_value():
                    return value
                self.init[field] = default_value

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

    def update(self, query: dict, set_data: dict):
        self.collection.update_one(
            json_bson(query),
            {
                '$set': json_bson(set_data)
             })
        print(query, set_data)

    def insert(self, doc):
        for field in self.init:
            if field not in doc:
                doc[field] = self.init[field]()
        self.collection.insert_one(
            doc
        )
        return doc

    def size(self, query: dict):
        return self.collection.find(query).count()


