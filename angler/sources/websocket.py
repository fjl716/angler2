from angler.channel import AChannel
from angler.source import ASource
from tornado import web, websocket
from random import random


class IndexHandler(web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.write("Web Socket working in /ws")


class WebSocketChannel(websocket.WebSocketHandler, AChannel):
    def data_received(self, chunk):
        pass

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        self.source = self.application.source
        self.source.on_line(self)

    def check_origin(self, origin):
        return True

    def send(self, data):
        self.write_message(data)

    def on_message(self, data):
        self.arrive(data)

    def on_close(self):
        self.close()


class WebSocketSource(ASource):
    def __init__(self, name, protocol,  port):
        ASource.__init__(self, name, protocol)
        self.port = port
        self.app = web.Application([
            (r'/', IndexHandler),
            (r'/ws', WebSocketChannel),
        ])
        self.angler = None
        self.app.source = self

    def packet_arrive(self, channel, data):
        self.container.arrive(channel.id, self.protocol.parse(data))

    def stop(self):
        pass

    def start(self, angler):
        self.angler = angler
        self.app.listen(self.port)
