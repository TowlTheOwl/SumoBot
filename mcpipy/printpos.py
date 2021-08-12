# This is to be stored in mcpipy file inside the minecraft directory, and to be run parallel to main.py to constantly feed in the information directly from minecraft client.

from mcpi.minecraft import *
import mcpi.block as block
import time
import math

def distance(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)**0.5
mc=Minecraft()
center=(-92,40,-92)#center of the training ring.
count=0
lastpos=(-90,0,-90)
digitpos=(-102, 10, -102)#where binary code will be pasted. Note that it will ALWAYS be pasted toward positive x axis.
p2dpos=(-102, 10, -100) #other player's binary code position; if it exists.
posblock=block.CLAY
f=-40 #make sure to change this if the opponent's n value has changed. 
p2rpos=(0,0,0) #initialize the opponent position tuple

while True:
    pos=mc.player.getPos()
    x, y, z=pos
    pval=bin((math.floor(x)+103)+(math.floor(y)-35)*529+(math.floor(z)+103)*23)[2:]
    for i in range(13-len(pval)):
        pval="0"+pval
    with open("D:\\Python\\Workspace\\test\\transmission.txt",'w') as f: #change to your directory
        f.write(f"{x}, {y}, {z}\n{distance((x,y,z), center)}")
    #place a block so other player can interact with my position
    if y<45 and y>35: #Change the x, y, z range according to the map. set this way for specific training environment made by us. Note that mcpi always rounds down, i.e. x=-98.2 -> x=-99.
        if x>-103 and x<-79 and z>-103 and z<-79:
            for i in range(13):
                if pval[i]=='1':
                    mc.setBlock((digitpos[0]+i,digitpos[1],digitpos[2]),posblock)
                else:
                    mc.setBlock((digitpos[0]+i,digitpos[1],digitpos[2]),block.AIR)
            
    
    #detect the position of other player
    p2val="" #clear/initialize the variable storing the position of the 
    for i in range(13):
        if mc.getBlock((p2dpos[0]+i,p2dpos[1],p2dpos[2]))==block.AIR: #will detect for anything other than the air block.
            p2val+='0'
        else:
            p2val+='1'
    p2rpos=(int(p2val,2)%23-103,int(int(p2val,2)/529)+35,int(int(p2val,2)%529/23)-103)
    mc.postToChat(p2rpos)
    count+=1
    lastpval=pval
    if y<20 or y>50:#clear any residue blocks.
        for i in range(len(pval)):
            mc.setBlock((digitpos[0]+i,digitpos[1],digitpos[2]),block.AIR)
    time.sleep(0.02)