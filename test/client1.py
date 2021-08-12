import pygame
from network import Network
import pickle

data = []

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
            data = game.get_data()
        except:
            run = False
            print("Couldn't get game")
            break


        #n.send(data)

main()