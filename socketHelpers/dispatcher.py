import time
from packet import Packet

DELAY_TIMER = 0.125
TIMEOUT = 10


class Dispatcher:
    def __init__(self, recipient, timeout=TIMEOUT):
        self.recipient = recipient
        self.running = False
        self.timeout = timeout

        self.buffer = b''

    def schedule(self, f): # chedule an event
        timeout = time.time() + self.timeout
        while (not self.running) and (time.time() < timeout):
            time.sleep(DELAY_TIMER)
        f()


    def recv_raw(self, data):
        self.buffer += data

        packet, self.buffer = Packet.pack(self.buffer)

        if packet != None : self.handle(packet)


    def handle(self, packet):
        print(packet)

    def _send(self, data):
        self.recipient.send(data)

    def send(self, packet):
        return self.schedule(lambda: self._send(packet.unpack()))
