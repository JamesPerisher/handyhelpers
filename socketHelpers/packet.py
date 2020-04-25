class Packet(object):
    START_SEQ = b'\x01\x00\x00\x02\x00\x00'
    def __init__(self, id, data=None):
        self.id   = b'' if (id  ==None) or (id  =="") else (id   if isinstance(id,   bytes) else   id.encode())
        self.data = b'' if (data==None) or (data=="") else (data if isinstance(data, bytes) else data.encode())

    def __repr__(self):
        return "<Packet(%s, %s)>"%("\"\"" if (self.id == "") or (self.id == None) else self.id, "\"\"" if (self.data == "") or (self.data == None) else self.data)

    def clear(self):
        self.data = b''

    def append(self, data):
        self.data = self.data + data

    def read(self):
        return self.data.decode()

    def read_raw(self):
        return self.data

    def get_id(self):
        return self.id.decode()

    def encode(self, data):
        return data

    def unpack(self):
        return self.id + b'\x00'*(16-len(self.id)) + self.encode(self.data)

    def pack(raw_data):
        return Packet(id=raw_data[0:16].replace(b'\x00', b''), data=raw_data[16::])
