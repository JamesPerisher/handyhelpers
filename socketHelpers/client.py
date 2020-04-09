from threading import Thread
from .dispatcher import Dispatcher
from .packet import Packet

import socket
import time

RECEIVE_BUFFER = 4096


class Client(Thread, Dispatcher):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Dispatcher.__init__(self, self.s)


        self.host = host
        self.port = port

        self.running = False

    def connect(self):
        self.s.connect((self.host, self.port))

    def close(self):
        self.s.close()

    def kill(self):
        self.running = False
        self.close()
        return "Killed connection"

    def run(self):
        self.connect()
        self.running = True

        while self.running:
            try:
                data = self.s.recv(RECEIVE_BUFFER)
            except Exception as e:
                self.kill()
                print("lost connection to server.")
                break
            self.recv_raw(data)
