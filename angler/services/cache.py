from angler.services.mongo import MongoDatabase


class Cache(object):
    def __init__(self, database):
        self.database = database

