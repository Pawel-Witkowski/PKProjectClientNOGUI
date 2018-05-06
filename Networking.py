import socket
from random import choice




class SocketData():
    def __init__(self):
        self.ip = socket.gethostbyname(socket.getfqdn())
        self.port = choice(range(10000,50000))