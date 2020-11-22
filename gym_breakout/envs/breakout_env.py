import numpy as np
import random
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import time
import os

class BreakoutEnv(gym.Env):
    _current_state = np.array
    _actions = np.array
    _walls = np.array
    _initial_state = np.array
    
    _rows = int
    _cols = int
    _wallsrows = int
    _states = []
    def __init__(self, rows = 7, cols = 5, wallsrows = 1):
        self._wallsrows = wallsrows
        self._rows = rows
        self._cols = cols
        
        self._walls = np.zeros((rows, cols))
        
        for i in range(self._wallsrows):                              #mette a 1 le posizioni in cui ci sono walls
            for j in range(cols):
                self._walls[i,j] = 1
        
        self._actions = ["left", "right", "stop"]
        
        self._initial_state = [2, 2, -1, 1, 0, self._walls]    #col palla, riga palla, direzione su col, direzione su righe, col barretta, situazione muri
        
        self._current_state = self._initial_state
        
        self._done = False
        
        self._ball_directions = [(-1,1), (-1,-1), (1,1), (1,-1)]
        
        self.generateState()
    
    def step(self, action):
        reward = 0
        info = 0
        
        self._walls[self._current_state[1],self._current_state[0]] = 0                      #pulisco la precedente posizione della palla dalla mappa
        
        if(self._current_state[1] >= self._rows-1):                                         #se sono sotto il livello della sbarretta    
            self._done = True
            reward -= 100
            return tuple(self._current_state), reward, self._done, info 
        
        if(self._walls[self._current_state[1]-1,self._current_state[0]] == 1 
        or ((self._current_state[0] == self._current_state[4] or self._current_state[0] == self._current_state[4] + 1) and self._current_state[1] == self._rows-2)
        or self._current_state[1] == 0):
            if(self._walls[self._current_state[1]-1,self._current_state[0]] == 1 and self._current_state[3]<0):             #se ho il blocco sopra e sto salendo
                self._walls[self._current_state[1]-1,self._current_state[0]] = 0
            elif(self._walls[self._current_state[1]-1,self._current_state[0]] == 1 and self._current_state[3]>0):           #se ho il blocco sopra e sto scendendo
                self._current_state[3] = self._current_state[3] * (-1)
            self._current_state[3] = self._current_state[3] * (-1)
        if(self._current_state[0] == self._cols-1 or self._current_state[0] == 0):          #se sono vicino ad un muro laterale
            self._current_state[2] = self._current_state[2] * (-1)
        
        t = tuple(self._walls[0])
        self._current_state[5] = t
        self._current_state[0] = self._current_state[0] + self._current_state[2]
        self._current_state[1] = self._current_state[1] + self._current_state[3]
        
        if self.checkWin():                                                                 #se ho vinto
            self._done = True
            reward +=100
            return tuple(self._current_state), reward, self._done, info 
        
        self.muovi_sbarretta(action)
        
        return tuple(self._current_state), reward, self._done, info 
        
    def muovi_sbarretta(self, action):
        if(action == "left" and self._current_state[4] != 0):
            self._current_state[4] -= 1
        elif(action == "right" and self._current_state[4] != self._cols-2):
            self._current_state[4] += 1
    
    def checkWin(self):
        esito = True
        for i in range (self._cols):
            for j in range (self._wallsrows):
                if self._walls[j,i] == 1:
                    esito = False
                    break
        return esito
    
    
    def render(self):
        graphic = np.full((self._rows, self._cols), '  ')
        graphic[self._current_state[1],self._current_state[0]] = 'o'
        
        for i in range (self._rows):
            for j in range (self._cols):
                if(self._walls[i,j] == 1):
                    graphic[i,j] = '[]'
        for i in range (self._cols):
            graphic[self._rows-1, i] = '  '
            
        graphic[self._rows-1, self._current_state[4]] = '---'
        graphic[self._rows-1, self._current_state[4]+1] = '---'
        for i in range (self._rows):
            print()
            for j in range (self._cols):
                print (graphic[i,j], end = '')
        print('\n\n\n\n\n\n\n')
        
        
    def nextState(self, state, action):
        self._current_state = list(state)
        nextState, reward, done, info = self.step(action)
        for i in range (self._cols):
            self._walls[0, i] = state[5][i]
        return nextState, reward, done, info

    def wallsCombinations(self, n):
        if n == 1:
            return [[1], [0]]
        else:
            comb = self.wallsCombinations(n-1)
            return list( map(lambda l: l + [1], comb)) + list(map(lambda l : l + [0], comb))
    
    def illegalState(self, state):
        return ((state[1] == 0 and state[3] > 0
                or(state[1] == self._rows-2 and (state[4] == state[0] or state[4]+1 == state[0]) and state[3] < 0)
                or(state[0] == 0 and state[2] > 0)
                or(state[0] == self._cols-1 and state[2] < 0)))
                
    def generateState(self):
        wallsComb = self.wallsCombinations(self._cols)
        for barpos in range(self._cols-1):
            for ballrow in range(self._rows):
                for ballcol in range(self._cols):
                    for (coldir, rowdir) in self._ball_directions:
                        for comb in wallsComb:
                            if not self.illegalState((ballcol, ballrow, coldir, rowdir, barpos, tuple(comb))):
                                self._states.append((ballcol, ballrow, coldir, rowdir, barpos, tuple(comb)))
                                
    def reset(self):
        for i in range(self._wallsrows):                              #mette a 1 le posizioni in cui ci sono walls
            for j in range(self._cols):
                self._walls[i,j] = 1
        self._done = False
        self._current_state = self._initial_state
    
    
    