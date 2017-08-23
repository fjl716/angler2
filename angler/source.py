from abc import ABCMeta, abstractmethod

from angler.channel import AChannel
from angler.protocol import AProtocol
from angler.service import IService


class ASource(IService):
    __metaclass__ = ABCMeta

    def __init__(self, name, protocol: AProtocol):
        IService.__init__(self, name)
        self.protocol = protocol
        self.container = None
        self.channels = dict()

    @abstractmethod
    def start(self, angler):
        pass

    @abstractmethod
    def stop(self):
        pass

    def on_line(self, channel: AChannel):
        self.channels[channel.id] = channel
        self.container.on_line(channel.id)

    def off_line(self, channel: AChannel):
        self.container.off_line(channel.id)
        del self.channels[channel.id]

    def arrive(self, channel, data):
        packet = self.protocol.parse(data)
        self.container.packet_arrive(channel.id, packet, [])

    def send(self, channel_id, packet):
        channel = self.channels.get(channel_id)
        if channel is not None:
            if packet.get('remote') is not None:
                del packet['remote']
            data = self.protocol.serialize(packet)
            if data is not None:
                channel.send(data)

