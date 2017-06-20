from functools import partial
from angler.service import IService


class Response(object):
    def __init__(self):
        self.packets = []

    def send(self, packet: dict):
        self.packets.append(packet)


class Container(IService):
    def __init__(self, name: str, source):
        IService.__init__(self, name)
        self.source = source
        self.angler = None
        self.events = dict()

    def container_send_packet(self, channel_id, packet):
        self.packet_arrive(channel_id, packet, [])

    def packet_arrive(self, channel_id, packet, path):
        for item in self.events.items():
            name = item[0]
            event = item[1]
            if name in path:
                continue
            if event.event.match(packet['event']) is None:
                continue
            response = Response()
            event.invoke(
                self.angler.services,
                packet,
                response
            )
            new_path = path[:]
            new_path.append(name)

            for packet in response.packets:
                equipment = packet.get('equipment')
                remote = packet.get('remote')
                if equipment is None:
                    if remote:
                        self.source.send(channel_id, packet)
                    self.packet_arrive(channel_id, packet, new_path)
                else:
                    self.angler.send(equipment, packet)

    def bind_channel(self, equipment, channel):
        path = '/angler/equipments/{0}/packets'.format(equipment)
        self.angler.zk.get_children(path, partial(self.container_send_packet, channel))

    def set_source(self, source):
        self.source = source

    def start(self, angler):
        self.angler = angler
        self.source.start(angler)

    def stop(self):
        self.source.stop()

    def on_line(self, channel_id: str):
        pass

    def off_line(self, channel_id: str):
        pass
