import time
from .packet import Packet

DELAY_TIMER = 0.125
TIMEOUT = 10


class Dispatcher:
    def __init__(self, recipient, timeout=TIMEOUT):
        self.recipient = recipient
        self.timeout = timeout

        self.buffer = b''

    def recv_raw(self, data):
        packet = Packet.pack(data)
        if packet : self.handle(packet)


    def handle(self, packet):
        print(packet)

    def _send(self, data):
        return self.recipient.send(data)

    def send(self, packet):
        return self._send(packet.unpack())
