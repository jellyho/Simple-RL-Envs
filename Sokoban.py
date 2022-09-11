import random
import numpy as np
import os
import time
from IPython.display import clear_output

class Sokoban:
  def __init__(self, grid_size=(6, 6), state_scale=2):
    self.size = grid_size
    self.state_scale = state_scale
    self.state_width = 1+ 2 * self.state_scale
    self.state_size = (self.state_width)**2
    self.action_size = 4
    self.codes = ['　', '▣', '■', 'О', 'Χ', '▨']
    self.matrix = [[0 for _ in range(self.size[0])] for i in range(self.size[1])]
    self.pos = [0, 0]
    self.box = [0, 0]
    self.goal = [0, 0]
    self.end = [0, 0]

    self.unavailable_reward = -1
    self.goal_reward = 1
    self.timestep_reward = -0.1

    self.max_timestep = 10000
    self.timestep = 0
    self.DELAY = 1

  def reset(self):
    self.matrix = [[0 for _ in range(self.size[0])] for i in range(self.size[1])]
    
    self.pos[0] = random.randrange(0, self.size[0])
    self.pos[1] = random.randrange(0, self.size[1])

    self.box[0] = self.randompick((1, self.size[0]-1), (self.pos[0],))
    self.box[1] = self.randompick((1, self.size[1]-1), (self.pos[1],))

    self.goal[0] = self.randompick((1, self.size[0]-1), (self.pos[0], self.box[0]))
    self.goal[1] = self.randompick((1, self.size[1]-1), (self.pos[1], self.box[1]))

    self.end[0] = self.randompick((1, self.size[0]-1), (self.pos[0], self.box[0], self.goal[0]))
    self.end[1] = self.randompick((1, self.size[1]-1), (self.pos[1], self.box[1], self.goal[1]))
    
    self.matrix[self.pos[1]][self.pos[0]] = 1
    self.matrix[self.box[1]][self.box[0]] = 2
    self.matrix[self.goal[1]][self.goal[0]] = 3
    self.matrix[self.end[1]][self.end[0]] = 4

    self.timestep = 0

    return self.get_state()

  def randompick(self, range, sub):
    done = False
    n = 0
    while not done:
      n = random.randrange(range[0], range[1])
      if not n in sub:
        done = True
    return n

  def get_state(self):
    state = [0] * (self.state_size)
    for i in range(0, self.state_width):
      if not self.pos[1] - self.state_scale + i in range(self.size[1]):
        for j in range(0, self.state_width):
          state[i * self.state_width + j] = 5
      else:
        for j in range(0, self.state_width):
          if not self.pos[0] - self.state_scale + j in range(self.size[0]):
            state[i * self.state_width + j] = 5
          else:
            state[i * self.state_width + j] = self.matrix[self.pos[1] - self.state_scale + i][self.pos[0] - self.state_scale + j]
        
    return state

  def step(self, action, show=False):
    self.timestep += 1
    if self.timestep > self.max_timestep:
      return self.get_state(), -1, True

    done = False
    next_state = None
    next_pos = [self.pos[0], self.pos[1]]
    next_box_pos = [self.box[0], self.box[1]]
    reward = 0

    def check(pos1, pos2):
      return pos1[0]==pos2[0] and pos1[1]==pos2[1]

    if action == 0:
      if self.pos[1] - 1 < 0:
        #reward += self.unavailable_reward
        pass
      else:
        next_pos = [self.pos[0], self.pos[1] - 1]
    elif action == 1:
      if self.pos[1] + 1 >= self.size[1]:
        #reward += self.unavailable_reward
        pass
      else:
        next_pos = [self.pos[0], self.pos[1] + 1]
    elif action == 2:
      if self.pos[0] - 1 < 0:
        #reward += self.unavailable_reward
        pass
      else:
        next_pos = [self.pos[0] - 1, self.pos[1]]
    elif action == 3:
      if self.pos[0] + 1 >= self.size[0]:
        #reward += self.unavailable_reward
        pass
      else:
        next_pos = [self.pos[0] + 1, self.pos[1]]

    if check(self.end, next_pos) or check(self.goal, next_pos):
      reward += self.unavailable_reward
      done = True
    elif check(self.box, next_pos): #박스와 충돌
      if action == 0:
        next_box_pos = [self.box[0], self.box[1] - 1]
      elif action == 1:
        next_box_pos = [self.box[0], self.box[1] + 1]
      elif action == 2:
        next_box_pos = [self.box[0] - 1, self.box[1]]
      elif action == 3:
        next_box_pos = [self.box[0] + 1, self.box[1]]
      
      if not next_box_pos[0] in range(0, self.size[0]) or not next_box_pos[1] in range(0, self.size[1]): #박스가 벽에 닿음
        reward += self.unavailable_reward
        done = True
        next_box_pos = [self.box[0], self.box[1]]
      elif check(next_box_pos, self.end):
        reward += self.unavailable_reward
        done = True
      elif check(next_box_pos, self.goal):
        reward += self.goal_reward
        done = True

    self.pos = next_pos
    self.box = next_box_pos
    self.matrix = [[0 for _ in range(self.size[0])] for i in range(self.size[1])]

    self.matrix[self.goal[1]][self.goal[0]] = 3
    self.matrix[self.end[1]][self.end[0]] = 4
    self.matrix[self.pos[1]][self.pos[0]] = 1
    self.matrix[self.box[1]][self.box[0]] = 2
    reward += self.timestep_reward
    if show:
      self.show(action, reward)      
    return self.get_state(), reward, done

  def show(self, action, reward):
    os.system('cls')
    clear_output()
    state = self.get_state()
    print(f"action:{action}    reward:{reward}    step:{self.timestep}/{self.max_timestep}")
    print(f"┏{'━'*(self.size[0])}┓    ┏{'━'*(self.state_width)}┓")
    for i in range(self.size[1]):
      print(f"┃", end="")
      for a in self.matrix[i]:
        print(self.codes[a], end="")
      print(f"┃    ", end="")
      if i in range(self.state_width):
        print(f"┃", end="")
        for a in range(self.state_width):
          print(self.codes[state[i * self.state_width + a]], end="")
        print(f"┃")
      elif i == self.state_width:
        print(f"┗{'━'*(self.state_width)}┛")
      else:
        print()
    print(f"┗{'━'*(self.size[0])}┛")
    time.sleep(self.DELAY)
