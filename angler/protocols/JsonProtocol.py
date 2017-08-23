import json

from bson import ObjectId

from angler.protocol import AProtocol


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

encoder = JSONEncoder()


class JSONDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict2object)

    def dict2object(self, obj):
        # for key in obj.keys():
            # value = obj[key]
            # if type(value) == dict:
            #     print(value)
        return obj


class JsonProtocol(AProtocol):
    def serialize(self, packet):
        return json.dumps(packet, cls=JSONEncoder, sort_keys=False)

    def parse(self, data):
        return json.loads(data, cls=JSONDecoder)
