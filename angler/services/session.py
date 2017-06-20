from angler.service import IService


class Session(IService):
    def __init__(self, database):
        IService.__init__(self, 'session')
        self.database = database

    def find_one(self, query):
        pass

    # self[key]
    def __getitem__(self, name):
        pass

    # del self[key]
    def __delitem__(self, name):
        pass

    # self[key] = val
    def __setitem__(self, name, val):
        pass

    def start(self, angler):
        self.database.start(angler)

    def stop(self):
        self.database.stop()
