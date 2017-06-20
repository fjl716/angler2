import json

from bson import ObjectId

from angler.protocol import AProtocol


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

encoder = JSONEncoder()


class JsonProtocol(AProtocol):
    def serialize(self, packet):
        return json.dumps(packet)

    def parse(self, data):
        return json.loads(data)
