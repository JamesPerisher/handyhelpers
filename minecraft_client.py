from pyCraft.minecraft import authentication
from minecraft.authentication import AuthenticationToken
from minecraft.networking.packets import serverbound
from minecraft.networking.connection import Connection
from minecraft.networking.packets.clientbound.play import ChatMessagePacket
from minecraft.networking.packets.serverbound.play import ChatPacket

import random, time, json
from threading import Timer




class minecraft_client():
    def __init__(self, username, password=None, server=None, versions=("1.12.2","1.12.2"), auto_connect=False):
        self.username = username
        self.password = password
        self.server = server
        self.versions = versions

        self.event = lambda x: print(x)

        self.auth_token = authentication.AuthenticationToken(username=self.username, access_token=self.password)
        print("authenticated: %s" %self.auth_token.authenticate(self.username, self.password, invalidate_previous=False))
        self.connection = Connection(self.server, auth_token=self.auth_token, allowed_versions=self.versions)

        self.connection.register_packet_listener(lambda x: self.print_chat(x), ChatMessagePacket)

        print(self.auth_token)
        print(self.connection)

        if auto_connect:
            self._loop_reconect()

    def _loop_reconect(self):
        Timer(30.0, self._loop_reconect).start()
        try:
            self.connect()
        except:
            pass


    def add_chat_event(self, event):
        self.event = event

    def connect(self):
        self.connection.connect()

    def disconnect(self, immediate=False):
        self.connection.disconnect(immediate=immediate)


    def send_message(self, message):
        if message.strip() == "" or message == None:
            return False
        packet = ChatPacket()
        packet.message = message
        self.connection.write_packet(packet)

    def print_chat(self, chat_packet):
        try:
            a = json.loads(chat_packet.json_data)
        except Exception as e:
            pass
        else:
            self.event(self.parse_chat(a))

    def parse_chat(self, chat_data):
        try:
            chat_data["extra"][0]["extra"]
            try:
                return (True, self.parse_chat(chat_data["extra"][0])[1])
            except Exception as e:
                print(e)
        except:
            try:
                return (False, "".join([x["text"] for x in chat_data["extra"]]))
            except:
                pass
            return




if __name__ == "__main__":

    c = minecraft_client(sys.argv[1], sys.argv[2], sys.argv[3])
    #c.add_chat_event()   # add event that gets called with one arge as array ===> (True|False, <message>) True is deathy message

    c.connect()

    while True:
        c.send_message(input("-"))
