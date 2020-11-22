import gym
import time
import os
import random
    
myEnv = gym.make('gym_breakout:breakout-v0')
termination = False
i = 0
while i<5 and not termination:
    myEnv.render()
    state, reward, termination, info = myEnv.step(myEnv._actions[random.randint(0,2)])
    i+=1
    time.sleep(0.1)
    os.system("cls")