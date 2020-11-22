import gym
import time
import os
import random

def policyEval(myEnv, policy, gamma, U):
    
    for state in myEnv._states:
        nextState, reward, done, info = myEnv.nextState(state, policy[state])
        U[state] = reward + gamma * U[nextState]
    return U
    

def policyIteration(myEnv):
    gamma = 1
    U = {s:0 for s in myEnv._states}
    policy = {s: myEnv._actions[random.randrange(2)] for s in myEnv._states}
    unchanged = False
    max_iteration = 3
        
    for i in range (max_iteration):
        if unchanged:
            break
        U = policyEval(myEnv, policy, gamma, U)
        unchanged = True
        
        for state in myEnv._states:
            bestaction = policy[state]
            nextState, reward, done, info = myEnv.nextState(state, policy[state])
            max = U[nextState]
            for action in myEnv._actions:
                nextState, reward, done, info = myEnv.nextState(state, action)
                if U[nextState] > max:
                    bestaction = action 
                    max = U[nextState]
                    unchanged = False
            policy[state] = bestaction
    return policy


def play(myEnv, policy):
    myEnv.reset()
    myEnv.render()
    myEnv._initial_state[5] = tuple(myEnv._initial_state[5][0])
    nextState, reward, done, info = myEnv.step(policy[tuple(myEnv._initial_state)])
    while not done:
        myEnv.render()
        time.sleep(0.1)
        os.system("cls")
        nextState, reward, done, info = myEnv.step(policy[nextState])
    
    myEnv.render()

def main():
    myEnv = gym.make('gym_breakout:breakout-v0')
    policy = policyIteration(myEnv)
    play(myEnv, policy)
    
if __name__ == "__main__":
    main()
    
    
    
    
    
    