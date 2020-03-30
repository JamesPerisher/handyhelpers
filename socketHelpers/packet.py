class Packet:
    def __init__(self, id=0, data=b''):
        self.id = id
        self.data = data

    def __repr__(self):
        return "<Packet(%s, %s)>"%("\"\"" if (self.id == "") or (self.id == None) else self.id, "\"\"" if (self.data == "") or (self.data == None) else self.data)

    def clear(self):
        self.data = b''

    def append(self, data):
        self.data = self.data + data

    def read(self):
        return self.data

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
