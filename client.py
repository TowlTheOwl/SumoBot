from network import Network
from random import randint
import pygame

clientNumber = 0

def make_tup(str):

    costList = str.strip('[]').split(", ")
    for i in costList:
        costList[costList.index(i)] = int(i)
    return costList


def main():

    clock = pygame.time.Clock()
    run = True
    try:
        n = Network()
    except Exception as e:
        print(e)
        quit()
    costList = [10, 10, 10, 20, 20, 20]

    while run:
        clock.tick(60)
        data = n.send(str(costList))
        costList = make_tup(data)
        print(costList)
        costList = [randint(10, 100), randint(10, 100), randint(10, 100), randint(10, 100), randint(10, 100), randint(10, 100)]


main()
