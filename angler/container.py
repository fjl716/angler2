from functools import partial

import sys

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
        for name, event in self.events.items():
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

            # try:
            #     event.invoke(
            #         self.angler.services,
            #         packet,
            #         response
            #     )
            # except:
            #     self.angler.logger.error(sys.exc_info()[0])

            new_path = path[:]
            new_path.append(name)
            for res_packet in response.packets:
                equipment = res_packet.get('equipment')
                remote = res_packet.get('remote')
                if res_packet.get('event') is None and len(event.result) == 1:
                    res_packet['event'] = event.result[0]
                if equipment is None:
                    if remote:
                        out_packet = {
                            'event': res_packet['event'],
                        }
                        if 'error' in res_packet:
                            out_packet['error'] = res_packet['error']
                        elif 'data' in res_packet:
                            out_packet['data'] = res_packet['data']
                        self.source.send(channel_id, out_packet)
                        self.packet_arrive(channel_id, res_packet, new_path)
                else:
                    self.angler.send(equipment, res_packet)

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
