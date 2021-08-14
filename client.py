import socket
from network import Network
from random import randint



def main():

    run = True
    print('connected')
    n = Network()
    print('network executed')
    player = int(n.getP())
    print(f'Player {player}')

    while run:
        data = []
        try:
            data = n.send("get")

        except:
            run = False
            print("Couldn't get game")
            break

        data = data.strip("[]").replace("'", "").split(', ')
        for i in range(len(data)):
            data[i] = randint(10, 99)
        try:
            n.send(str(data))
        except:
            print("Couldn't send data")

main()
