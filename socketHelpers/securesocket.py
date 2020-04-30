from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import socket


class RSASocket(socket.socket):
    def __init__(self, *args, block_size=AES.block_size, key_size=32, **kwargs):
        super().__init__(*args, **kwargs)
        self.masterkey = None
        self.block_size = block_size
        self.key_size = key_size

    @classmethod
    def copy(cls, sock):
        fd = socket.dup(sock.fileno())
        copy = cls(sock.family, sock.type, sock.proto, fileno=fd)
        copy.settimeout(sock.gettimeout())
        return copy

    def pad(self, data):
        return data + (self.block_size - len(data) % self.block_size) * bytes([self.block_size - len(data) % self.block_size])
    def unpad(self, data):
        return data[:-ord(data[len(data)-1:])]

    def generate_rsa(self, privkey=None):
        privkey = privkey if privkey else RSA.generate(1024, Random.new().read)
        return privkey.publickey(), privkey

    def generate_aes(self):
        self.masterkey = Random.new().read(self.key_size)

    def accept(self):
        conn, addr = super().accept()
        return RSASocket.copy(conn).server_protocal(addr)

    def connect(self, address):
        return self.client_protocal(super().connect(address))

    def encrypt(self, data):
        raw = self.pad(data)
        iv = Random.new().read(16)
        cipher = AES.new(self.masterkey, AES.MODE_CBC, iv)
        return (iv + cipher.encrypt( raw ))

    def decrypt(self, data):
        iv = data[:16]
        cipher = AES.new(self.masterkey, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(data[16:]))


    def server_protocal(self, addr):
        pupkey, privkey = self.generate_rsa()
        super().send(pupkey.export_key('PEM'))

        self.masterkey = PKCS1_OAEP.new(privkey).decrypt(super().recv(4096))
        return self, addr


    def client_protocal(self, conn):
        self.generate_aes()
        super().send(PKCS1_OAEP.new(RSA.import_key(super().recv(4096))).encrypt(self.masterkey))
        return conn


    def send(self, data):
        e = self.encrypt(data)
        return super().send(e)

    def recv(self, *args, **kwargs):
        return self.decrypt(super().recv(*args, **kwargs))
