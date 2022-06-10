import numpy as np
import pandas as pd
import time
from collections import defaultdict
import random
import os

class ChopStick:
  def __init__(self):
    self.matrix = [1, 1, 1, 1]
    self.state = self.matrix.copy()
    self.unavailable_reward = -1
    self.winning_reward = 1
    self.state_size = 4
    self.action_size = 10
    self.DELAY = 1
    self.code_to_str_1 = ["    ", "  | ", " |/ ", " ||/", "||//"]
    self.code_to_str_2 = ["    ", " |  ", " /| ", "/|| ", "//||"]

  def reset(self):
    self.matrix = [1, 1, 1, 1]
    self.state = self.matrix.copy()

    return self.state

  def swap(self):
    temp = self.matrix.copy()
    self.matrix[0] = temp[3]
    self.matrix[1] = temp[2]
    self.matrix[2] = temp[1]
    self.matrix[3] = temp[0]

  def step(self, side, action, show=False):
    reward = 0
    next_state = self.state.copy()
    done = False
    active = True

    if side==2:
      self.swap()
    
    if action==6: #각 행동에 대해서 행동이 불가능할경우 패널티
      if self.matrix[0]==0 or self.matrix[2]==0:
        reward+= self.unavailable_reward
        active = False
      else:
        temp = self.matrix[0] + self.matrix[2]
        if temp >= 5:
          self.matrix[0] = 0
        else:
          self.matrix[0] = temp
    
    elif action==7:
      if self.matrix[1]==0 or self.matrix[2]==0:
        reward+= self.unavailable_reward
        active = False
      else:
        temp = self.matrix[1] + self.matrix[2]
        if temp >= 5:
          self.matrix[1] = 0
        else:
          self.matrix[1] = temp

    elif action==8:
      if self.matrix[0]==0 or self.matrix[3]==0:
        reward+= self.unavailable_reward
        active = False
      else:
        temp = self.matrix[0] + self.matrix[3]
        if temp >= 5:
          self.matrix[0] = 0
        else:
          self.matrix[0] = temp

    elif action==9:
      if self.matrix[1]==0 or self.matrix[3]==0:
        reward+= self.unavailable_reward
        active = False
      else:
        temp = self.matrix[1] + self.matrix[3]
        if temp >= 5:
          self.matrix[1] = 0
        else:
          self.matrix[1] = temp

    else: # 내손에서 내손으로 옮기기
      actDict = {0:-1, 1:-2, 2:-3, 3:1, 4:2, 5:3}
      tempL = self.matrix[2] + actDict[action]
      tempR = self.matrix[3] - actDict[action]

      if tempL==self.matrix[3] and tempR==self.matrix[2]:
        reward += self.unavailable_reward
        active = False
      elif tempL < 0 or tempR < 0 or tempR > 4 or tempL > 4:
        reward += self.unavailable_reward
        active = False
      else:
        self.matrix[2] = tempL
        self.matrix[3] = tempR

    if self.matrix[2]==0 and self.matrix[3]==0:
      done = True
    if self.matrix[0]==0 and self.matrix[1]==0:
      done = True
      reward += self.winning_reward

    next_state = self.matrix.copy()

    if side==2:
      self.swap()

    if show:
      self.show(side, action, reward)

    return next_state, reward, active, done

  def show(self, side, act, reward):
    os.system('cls')
    print(f"S:{side},A:{act},R:{reward}")
    print("----------")
    print(" []    []  ")
    print(f"{self.code_to_str_2[self.matrix[0]]}  {self.code_to_str_2[self.matrix[1]]}")
    print("")
    print("")
    print("")
    print(f"{self.code_to_str_2[self.matrix[2]]}  {self.code_to_str_2[self.matrix[3]]}")
    print(" []    []  ")
    print("----------")
    time.sleep(self.DELAY)
