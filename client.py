from network import Network
from random import randint

clientNumber = 0

def make_tup(str):

    costList = str.strip('[]').split(", ")
    for i in costList:
        costList[costList.index(i)] = int(i)
    return costList


def main():
    run = True
    n = Network()
    costList = [10, 10, 10, 20, 20, 20]

    while run:
        data = n.send(str(costList))
        costList = make_tup(data)
        print(costList)
        costList = [randint(10, 100), randint(10, 100), randint(10, 100), randint(10, 100), randint(10, 100), randint(10, 100)]


main()