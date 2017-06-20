from angler.protocols.JsonProtocol import JsonProtocol
#
# protocol_factory = {
#     'json': lambda conf:
#     JsonProtocol()
# }

protocol_map = dict()
protocol_map['json'] = lambda conf: JsonProtocol()


def protocol_factory(conf):
    factory = protocol_map.get(conf['type'])
    if factory is not None:
        return factory(conf)
    return None
