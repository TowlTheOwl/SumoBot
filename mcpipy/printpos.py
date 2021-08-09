# This is to be stored in mcpipy file inside the minecraft directory, and to be run parallel to main.py to constantly feed in the information directly from minecraft client. (run on both clients when playing on 2 different accounts.)

from mcpi.minecraft import *
import mcpi.block as block
import time

def distance(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)**0.5
mc=Minecraft()
center=(0,34,0)
count=0
lastpos=(-90,0,-90)
n=20 #make sure to have difference in this variable to prevent position not saving correctly in the map.
while True:
    pos=mc.player.getPos()
    x, y, z=pos
    with open("D:\\Python\\Workspace\\test\\transmission.txt",'w') as f: #change to your directory where the python script runs, but make sure to name the txt file the same way.
        f.write(f"{x}, {y}, {z}\n{distance((x,y,z), center)}")
    if count==5:
        #mc.postToChat(f"{x}, {y}, {z}\n{distance((x,y,z), center)}")
        count=0
    #place a block so other player can interact with my position
    if y<45 and y>35: #Change the x, y, z range according to the map. set this way for specific training environment made by us.
        if x>-104 and x<-79 and z>-104 and z<-79:
            if mc.getBlock(lastpos)==block.CLAY:
                mc.setBlock(lastpos, block.AIR)
            if mc.getBlock((x,y-n,z))==0:
                mc.setBlock((x,y-n,z), block.CLAY)
    #detect the position of other player. Note that opponent being more than 3 euclidean blocks away 
    count+=1
    lastpos=(x,y-n,z)
    time.sleep(0.02)
