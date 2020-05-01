import time
from .packet import Packet

DELAY_TIMER = 0.125
TIMEOUT = 10


class Dispatcher(object):
    kill = lambda self,msg: "Dispatcher killed via: %s"%msg

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
        try:
            return self._send(packet.unpack())
        except (ConnectionAbortedError, ConnectionResetError, ConnectionRefusedError, OSError) as e:
            print(self.kill("No connection to server."))
            return False
