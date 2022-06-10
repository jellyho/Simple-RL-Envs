import numpy as np
import pandas as pd
import time
from collections import defaultdict
import random
import os

class TicTacToe:
  def __init__(self):
    self.matrix = [0, 0, 0, 0, 0, 0, 0, 0, 0] #게임 정보 담을 변수
    self.answers = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]] #한줄 맞춰지는 조건
    self.state = self.matrix.copy()
    self.unavailable_reward = -1
    self.winning_reward = 1
    self.code_to_str = [" ", "O", "X"]
    self.state_size = 8
    self.action_size = 8
    self.DELAY = 1

  def reset(self):
    self.matrix = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.state = self.matrix.copy()
    return self.state

  def swap(self): # O와 X를 바꾸는 함수
    for i in range(9):
      a = self.matrix[i]
      if a==1:
        self.matrix[i] = 2
      elif a==2:
        self.matrix[i] = 1
  
  def step(self, side, action, show=False):
    reward = 0
    next_state = self.state
    done = False
    active = True

    if self.matrix[action]==0: #빈 공간에 돌 놓기
      self.matrix[action] = side

      next_state = self.matrix.copy()

      for ans in self.answers: #줄이 완성되어서 게임이 끝났는가?
        temp = [3, 4, 5]
        for a in range(3):
          if self.matrix[ans[a]]!=0:
            temp[a] = self.matrix[ans[a]]
          else:
            break
        if temp[0]==temp[1] and temp[1]==temp[2]:
          done = True
          reward += self.winning_reward
          break
    else:
      reward += self.unavailable_reward
      active = False
    
    temp = True
    for i in range(9): #9칸이 모두 다 찼는가?
      if self.matrix[i] == 0:
        temp = False
    if temp:
      done = True
    if show:
      self.show(side, action, reward)

    return next_state, reward, active, done
  
  def show(self, side, act, reward):
    os.system('cls')
    print(f"Side:{side}, A:{act}, R:{reward}")
    print("---------")
    print("|",self.code_to_str[self.matrix[0]],self.code_to_str[self.matrix[1]],self.code_to_str[self.matrix[2]],"|")
    print("|",self.code_to_str[self.matrix[3]],self.code_to_str[self.matrix[4]],self.code_to_str[self.matrix[5]],"|")
    print("|",self.code_to_str[self.matrix[6]],self.code_to_str[self.matrix[7]],self.code_to_str[self.matrix[8]],"|")
    print("---------")
    time.sleep(self.DELAY)
