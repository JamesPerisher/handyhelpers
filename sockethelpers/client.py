from customthreading import KillableThread
from .securesocket import RSASocket
from .dispatcher import Dispatcher
from .packet import Packet

import socket
import time

RECEIVE_BUFFER = 4096


class Client(KillableThread, Dispatcher):
    def __init__(self, host, port):
        KillableThread.__init__(self)
        self.s = RSASocket(socket.AF_INET, socket.SOCK_STREAM)
        Dispatcher.__init__(self, self.s)


        self.host = host
        self.port = port

    def connect(self):
        try:
            self.s.connect((self.host, self.port))
        except ConnectionRefusedError:
            print(self.kill("Connection refused"))

    def close(self):
        self.s.close()

    def kill(self, reason):
        super().kill()
        self.close()
        return reason

    def run(self):
        while True:
            try:
                data = self.s.recv(RECEIVE_BUFFER)
            except Exception as e:
                self.kill("lost connection to server.")
                break
            self.recv_raw(data)

    def start(self):
        c = self.connect()
        super().start()
        return c
