import numpy as np
import random
import time
from google.colab import output
from IPython.display import clear_output 
import os

"""
version : 2
"""

class GridWorld:
  def __init__(self, width, height, state_mode="relative", relative_state_width=2, start=[0, 0], goal=None, start_method="left_top", goal_method="right_bottom", goal_included_in_state=True, dir_included_in_state=True):
    self.width = width
    self.height = height
    self.action_size = 5
    self.state_size = 2
    self.act_to_str = ["O","^","v","<",">"]
    self.str_to_act = {"O":0, "^":1, "v":2, "<":3, ">":4}
    self.state_mode = state_mode

    self.matrix = [["#" for j in range(self.width)] for i in range(self.height)]
    self.state = start
    self.pos = start

    self.goal = goal
    self.start = start
    self.start_method = start_method
    self.goal_method = goal_method

    self.obstacle_reward = -1
    self.goal_reward = 1
    self.alive_reward = -0.1
    self.unavailable_reward = -1
    self.DELAY = 1

    self.giis = goal_included_in_state
    self.diis = dir_included_in_state

    self.relative_state_width = relative_state_width

    self._obstacles = []
    self.obstacles = []

  def reset_obstacles(self):
    self.obstacles = [obs for obs in self._obstacles]

  def reset_start_goal(self): #call after reset obstacles
    if self.start_method == "left_top":
      self.start = [0, 0]
      self.pos = self.start
    elif self.start_method == "random":
      check = False
      x = 0
      y = 0
      while not check:
        check = True
        x = random.randrange(0, self.width)
        y = random.randrange(0, self.height)
        for obs in self._obstacles:
          if x==obs[0] and y==obs[1]:
            check = False
        self.start = [x, y]
        self.pos = self.start
    else:
      raise Exception("Undefined Start Method")

    if self.goal_method == "right_bottom":
      self.goal = [self.width-1, self.height-1]
    elif self.goal_method == "random":
      check = False
      x = 0
      y = 0
      while not check:
        check = True
        x = random.randrange(0, self.width)
        y = random.randrange(0, self.height)
        for obs in self._obstacles:
          if (x==obs[0] and y==obs[1]) or (x==self.start[0] and y==self.start[1]):
            check = False
        self.goal = [x, y]
    else:
      raise Exception("Undefined Goal Method")

  def add_obstacles(self, posx, posy, dir=0, method="reflect", include_state=True): # 정지:O 상:^ 하:v 좌:< 우:> #method: "reflect", ["O","^","v","<",">"]
    self._obstacles.append([posx, posy, dir, method, include_state])
    self.reset_state()

  def refresh_matrix(self):
    self.matrix = [["#" for j in range(self.width)] for i in range(self.height)]
    for obs in self.obstacles:
      self.matrix[obs[1]][obs[0]] = self.act_to_str[obs[2]]

  def reset_state(self):
    self.reset_obstacles()
    self.reset_start_goal()
    self.refresh_matrix()

    if self.state_mode == "absolute":
      self.state = [self.pos[0], self.pos[1]]
    elif self.state_mode == "relative":
      self.state = [0 for _ in range((self.relative_state_width*2+1)**2)]

    if self.giis:
      self.state += [self.goal[0]-self.pos[0], self.goal[1]-self.pos[1]]

    if self.state_mode == "absolute":
      for obs in self.obstacles:
        if obs[4]:
          if self.diis:
            self.state += [obs[0]-self.state[0],obs[1]-self.state[1], obs[2]]
          else:
            self.state += [obs[0]-self.state[0],obs[1]-self.state[1]]
    elif self.state_mode == "relative": # 0은 빈공간 1은 벽 2는 장애물 3이 도착
      for i in range((self.relative_state_width*2+1)**2):
        x = i % (self.relative_state_width*2 + 1)
        y = i // (self.relative_state_width*2 + 1)
        x += self.pos[0] - self.relative_state_width
        y += self.pos[1] - self.relative_state_width

        if x < 0 or y < 0 or x >=self.width or y>=self.height:
          self.state[i] = 9
        elif x==self.goal[0] and y==self.goal[1] and self.giis:
          self.state[i] = 8
        elif self.matrix[y][x] in self.act_to_str:
          if not self.diis:
            self.state[i] = 7
          else:
            self.state[i] = self.str_to_act[self.matrix[y][x]]

    self.state_size = len(self.state)

  def refresh_state(self):
    if self.state_mode == "absolute":
      self.state = [self.pos[0], self.pos[1]]
    elif self.state_mode == "relative":
      self.state = [0 for _ in range((self.relative_state_width*2+1)**2)]

    if self.giis:
      self.state += [self.goal[0]-self.pos[0], self.goal[1]-self.pos[1]]

    if self.state_mode == "absolute":
      for obs in self.obstacles:
        if obs[4]:
          if self.diis:
            self.state += [obs[0]-self.state[0],obs[1]-self.state[1], obs[2]]
          else:
            self.state += [obs[0]-self.state[0],obs[1]-self.state[1]]
    elif self.state_mode == "relative": # 0은 빈공간 1은 벽 2는 장애물 3이 도착
      for i in range((self.relative_state_width*2+1)**2):
        x = i % (self.relative_state_width*2 + 1)
        y = i // (self.relative_state_width*2 + 1)
        x += self.pos[0] - self.relative_state_width
        y += self.pos[1] - self.relative_state_width

        if x < 0 or y < 0 or x >=self.width or y>=self.height:
          self.state[i] = 9
        elif x==self.goal[0] and y==self.goal[1] and self.giis:
          self.state[i] = 8
        elif self.matrix[y][x] in self.act_to_str:
          if not self.diis:
            self.state[i] = 7
          else:
            self.state[i] = self.str_to_act[self.matrix[y][x]]

  def reset(self):
    self.reset_state()
    return self.state

  def show(self, state, reward, action):
    clear_output()
    if self.state_mode=="absolute":
      print(f"state:{state}, reward:{reward}, action:{self.act_to_str[action]}")
    elif self.state_mode=="relative":
      print("state:")
      for i in range(self.relative_state_width*2+1):
        for j in range(self.relative_state_width*2+1):
          print(state[i*(self.relative_state_width*2+1)+j], end=" ")
        print()
      if self.giis:
        print(f"[{state[-2]}, {state[-1]}]")
      print(f"reward:{reward}, action:{self.act_to_str[action]}")

    print("-"+"-"*self.width*2+"-")

    for l in range(self.height):
      print("|", end="")
      for m in range(self.width):
        if self.pos[0] == m and self.pos[1] == l:
          print("A", end=" ")
        elif self.goal[0] == m and self.goal[1] == l:
          print("G", end=" ")
        elif self.start[0] == m and self.start[1] == l:
          print("S", end=" ")
        else:
          print(self.matrix[l][m], end=" ")
      print("|")

    print("-"+"-"*self.width*2+"-")
    time.sleep(self.DELAY)

  def step(self, action, show=False):
    for obs in self.obstacles:
      #좌표 업데이트
      if obs[2] == 0:
        pass
      elif obs[2] == 1 and not obs[1] == 0:
        obs[1] -= 1
      elif obs[2] == 2 and not obs[1] == self.height-1:
        obs[1] += 1
      elif obs[2] == 3 and not obs[0] == 0:
        obs[0] -= 1
      elif obs[2] == 4 and not obs[0] == self.width-1:
        obs[0] += 1
      else:
        pass

      #다음 행동 구하기
      if obs[3]=="reflect":
        if obs[2] == 0:
          pass
        elif obs[2] == 1 and obs[1] == 0:
          obs[2] = 2
        elif obs[2] == 2 and obs[1] == self.height-1:
          obs[2] = 1
        elif obs[2] == 3 and obs[0] == 0:
          obs[2] = 4
        elif obs[2] == 4 and obs[0] == self.width-1:
          obs[2] = 3
        else:
          pass
      elif obs[3]=="random":
        obs[2] = random.randrange(0, 5)
      #matrix에 추가
    self.refresh_matrix()


    # 에이전트 움직이기
    next_pos = [self.pos[0], self.pos[1]]
    reward = 0
    done = False

    if action == 0:
      next_pos = next_pos
    elif action == 1 and not self.pos[1]==0:
      next_pos[1] -= 1
    elif action == 2 and not self.pos[1]==self.height-1:
      next_pos[1] += 1
    elif action == 3 and not self.pos[0]==0:
      next_pos[0] -= 1
    elif action == 4 and not self.pos[0]==self.width-1:
      next_pos[0] += 1
    else:
      next_pos = next_pos
      reward += self.unavailable_reward

    #보상, 완료 여부

    if self.matrix[next_pos[1]][next_pos[0]] in self.act_to_str:
      reward += self.obstacle_reward
      done = False
    elif next_pos[0]==self.goal[0] and next_pos[1]==self.goal[1]:
      reward += self.goal_reward
      done = True
    else:
      pass
    reward += self.alive_reward

    self.pos = next_pos
    self.refresh_state()

    if show:
      env.show(self.state, reward, action)

    return self.state, reward, done
