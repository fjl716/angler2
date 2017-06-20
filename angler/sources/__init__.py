from angler.sources.websocket import WebSocketSource

source_map = dict()
source_map['websocket'] = lambda conf, protocol: WebSocketSource('websocket', protocol, int(conf['port']))


def source_factory(conf, protocol):
    factory = source_map.get(conf['type'])
    if factory is not None:
        return factory(conf, protocol)
    return None
