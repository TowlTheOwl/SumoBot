import socket
from threading import Thread
from database import Database

server = '10.0.0.24'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("waiting for a connection, server started")

game = None

def threaded_client(conn, p, game):
    conn.send(str.encode(str(p)))
    print('sent p')

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if game is not None:
                if not data:
                    break
                else:
                    if data != "get":
                        game.input_data(data)

                    conn.sendall(str.encode(str(game.get_data())))
        except:
            break

    print("lost connection")
    conn.close()

gameid = 1
currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("connected to:", addr)
    if currentPlayer == 0:
        game = Database(gameid)

    currentPlayer += 1

    client = Thread(target=threaded_client, args=(conn, currentPlayer, game))
    client.start()