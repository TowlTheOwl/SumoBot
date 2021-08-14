import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ('10.0.0.24', 5555)
        self.p = self.connect_to_network()

    def getP(self):
        return self.p

    def connect_to_network(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)