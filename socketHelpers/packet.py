class Packet:
    def __init__(self, id, data):

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

    def get_id(self):
        return self.id.decode()

    def unpack(self):
        return b'\x01' + self.id + b'\x02' + self.data + b'\x03\x04'

    def pack(raw_data):
        id = b''
        isid = False
        data = b''
        isdata = False

        for i in raw_data:
            i = bytes([i])
            if i == b'\x01' : isid   = True ;                continue
            if i == b'\x02' : isid   = False; isdata = True; continue
            if i == b'\x03' : isdata = False;                continue
            if i == b'\x04' :                                break

            if isdata : data += i; raw_data = raw_data[1::]; continue
            if isid   : id   += i; raw_data = raw_data[1::]; continue

        if id == b'' and data == b'': return None, raw_data

        return Packet(id=id, data=data), raw_data[4::]
