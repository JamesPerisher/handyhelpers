from threading import Thread
from .dispatcher import Dispatcher
from .packet import Packet

import socket
import time

RECEIVE_BUFFER = 4096
MAX_CONNECT = 1000000000

class ConnectionServer(dict, Thread):
    def __init__(self, host, port, max_connect=MAX_CONNECT):
        Thread.__init__(self)
        dict.__init__(self)
        self.CONNECTION = Connection
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.host = host
        self.port = port
        self.max_connect = max_connect

    def __repr__(self):
        return "<ConnectionServer(%s)>"%super().__repr__()

    def __hash__(self):
        return super(dict).__hash__()

    def __setitem__(self, key, item):
        if isinstance(item, Connection) : return super().__setitem__(key, item)
        raise TypeError("Connection server can only contain active connctions.")


    def update(self, *args, **kwargs):
        if isinstance(item, Connection) : return super().update(key, item)
        raise TypeError("Connection server can only contain active connctions.")

    def listen(self):
        self.s.bind((self.host, self.port))
        self.s.listen(self.max_connect)

    def connect_event(self, conn):
        pass

    def connect(self, conn, addr):
        self[addr] = self.CONNECTION(conn, addr, self)
        print(self)
        self[addr].start()
        self.connect_event(self[addr])

    def disconnect_event(self, addr, reason):
        pass


    def disconnect(self, addr, reason):
        self.pop(addr)
        self.disconnect_event(addr, reason)


    def run(self):
        self.listen()
        while True:
            try:
                conn, addr = self.s.accept()
                self.connect(conn, addr)
            except Exception as e:
                print(type(e), e)


class Connection(Thread, Dispatcher):
    def __init__(self, s, addr, lister=None):
        Thread.__init__(self)
        Dispatcher.__init__(self, s)
        self.s = s
        self.addr = addr
        self.lister = lister

    def close(self):
        self.s.close()

    def kill(self):
        self.running = False
        self.close()

    def run(self):
        self.running = True
        try:
            while self.running:
                self.recv_raw(self.s.recv(RECEIVE_BUFFER))
            self.s.close()
        except Exception as e:
            dc = "client disconnected: %s %s" %(type(e), e)
            if self.lister != None : self.lister.disconnect(self.addr, dc); print(dc)

            self.kill()
