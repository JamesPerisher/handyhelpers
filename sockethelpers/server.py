from customthreading import KillableThread
from .securesocket import RSASocket
from collections import OrderedDict
from .dispatcher import Dispatcher
from .packet import Packet

import socket
import time

RECEIVE_BUFFER = 4096
MAX_CONNECT = 1000000000


class Connection(KillableThread, Dispatcher):
    def __init__(self, s, addr, lister=None):
        KillableThread.__init__(self)
        Dispatcher.__init__(self, s)
        self.s = s
        self.addr = addr
        self.lister = lister

    def close(self):
        self.s.close()

    def kill_event(self):
        pass

    def kill(self, dc):
        if self.lister: self.lister.disconnect(self.addr, dc)
        self.kill_event()
        self.close()
        super().kill()
        return "Killed connection (%s)."%dc

    def run(self):
        try:
            while True:
                self.recv_raw(self.s.recv(RECEIVE_BUFFER))
            self.s.close()
        except Exception as e:
            dc = "client disconnected: %s %s" %(type(e), e)
            self.kill(dc)


class ConnectionServer(KillableThread, OrderedDict):
    CONNECTION = Connection
    def __init__(self, host, port, max_connect=MAX_CONNECT):
        KillableThread.__init__(self)
        dict.__init__(self)
        self.s = RSASocket(socket.AF_INET, socket.SOCK_STREAM)

        self.host = host
        self.port = port
        self.max_connect = max_connect

    def copy(self):
        return OrderedDict(self)

    def __repr__(self):
        return "<ConnectionServer(%s)>"%OrderedDict.__repr__(self)

    def __hash__(self):
        return super(dict).__hash__()

    def __setitem__(self, key, item):
        if isinstance(item, Connection) : return super().__setitem__(key, item)
        raise TypeError("Connection server can only contain active connctions.")

    def key(key, addr):
        return "%s:%s"%addr

    def update(self, *args, **kwargs):
        if isinstance(item, Connection) : return super().update(key, item)
        raise TypeError("Connection server can only contain active connctions.")

    def listen(self):
        self.s.bind((self.host, self.port))
        self.s.listen(self.max_connect)

    def connect_event(self, conn):
        pass

    def connect(self, conn, addr):
        self[self.key(addr)] = self.CONNECTION(conn, addr, self)
        print(self)
        self[self.key(addr)].start()
        self.connect_event(self[self.key(addr)])

    def disconnect_event(self, addr, reason):
        pass


    def disconnect(self, addr, reason):
        try:
            self.pop(self.key(addr))
        except KeyError: # disconnected between now and when asked to
            pass
        self.disconnect_event(addr, reason)

    def distribute_packet(self, packet):
        for i in self:
            self[i].send(packet)

        return "Distibuted packet across clients."


    def run(self):
        self.listen()
        while True:
            try:
                conn, addr = self.s.accept()
                self.connect(conn, addr)
            except Exception as e:
                print(type(e), e)
