import math
def convfloat(stringlist):
    dummy=[]
    for i in stringlist:
        dummy.append(float(i))
    return dummy
def reward(action_list, reward_list, dist_center, dist_op, facingHeat, enemyFacingHeat, airtime, wastedhit, *WorL):
    """
    reward_list will contain the tuples of reward and the time of the action which was taken.
    **wastedhit parameter is not in use.
    """
    if len(action_list)<len(reward_list)+1:
        #when all actions been evaluated
        assert len(action_list)==len(reward_list),"reward function ran in an immature state."
        return None #skip the function for now
    rtime=action_list[-1*(len(action_list)-len(reward_list))][0]
    reward=0
    ###ALL OF THESE ARE HYPERPARAMETERS
    if dist_center<=2:
        reward+=-1*(dist_center**2)+4
        reward+=0.5*dist_op
    else:
        reward+=-2*(dist_center**2)+8
        reward-=dist_op-2
    if facingHeat>1: #the agent is looking inside the enemy hitbox
        reward+=facingHeat-1
    elif facingHeat>=0.1:#logarithmic punishment for looking outside the hitbox
        reward+=4*math.log(facingHeat)
    else: #avoid facingHeat factor from taking over when it is near 0 or causing error when it is equal to 0
        reward-=10
    if enemyFacingHeat<1: #when the enemy can't look at your hitbox
        reward+=0.5
    else:
        reward-=1
    if airtime>=0.5: #when you were hit and the airtime increases- sign that you are vulnerable
        reward-=4*int(airtime*2)#efficient version of airtime/0.5
    reward_list.append((rtime,reward))
    #-----
    if len(WorL)==1:
        ftime=action_list[-1][0]
        ###Win/Loss reward handling:
        ###Latest 0.5 second does not receive extra reward (while the enemy/agent is falling after detemined fail)
        ###For actions taken in previous 4.5 seconds would receive maximum reward
        ###exponentially decreasing rewards given in next
        if bool(WorL[0])==True:
            #Case of win
            reward_slice=[x for x in reward_list if (x[0]>=ftime-5 and x[0]<=ftime-0.5)]
            for i_time, i_reward in reward_slice:
                if i_time>=ftime-2:
                    reward_list[reward_list.index((i_time, i_reward))]+=1500
                else:
                    reward_list[reward_list.index((i_time, i_reward))]+=5000*((1/(ftime-i_time))-0.2)
        else:
            #Case of loss
            reward_slice=[x for x in reward_list if (x[0]>=ftime-5 and x[0]<=ftime-0.5)]
            for i_time, i_reward in reward_slice:
                if 2>=ftime-i_time:
                    reward_list[reward_list.index((i_time, i_reward))]-=1500
                else:
                    reward_list[reward_list.index((i_time, i_reward))]-=500*((1/(ftime-i_time))-0.2)
    elif len(WorL)>1:
        raise BaseException("Invalid input")
    #return updated reward list
    return reward_list
if __name__=="__main__":
    print('yes.')
