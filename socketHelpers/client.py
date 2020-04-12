from customThreading import KillableThread
from .dispatcher import Dispatcher
from .packet import Packet

import socket
import time

RECEIVE_BUFFER = 4096


class Client(KillableThread, Dispatcher):
    def __init__(self, host, port):
        KillableThread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dispatcher.__init__(self, self.s)


        self.host = host
        self.port = port

    def connect(self):
        self.s.connect((self.host, self.port))

    def close(self):
        self.s.close()

    def kill(self):
        super().kill()
        self.close()
        return "Killed connection"

    def run(self):
        self.connect()

        while True:
            try:
                data = self.s.recv(RECEIVE_BUFFER)
            except Exception as e:
                self.kill()
                print("lost connection to server.")
                break
            self.recv_raw(data)
