import numpy as np
import random
import time
from google.colab import output
from IPython.display import clear_output 

class GridWorld:
  def __init__(self, width, height, goal=None):
    self.width = width
    self.height = height
    self.matrix = [["#" for j in range(self.width)] for i in range(self.height)]
    self.act_to_str = ["O","^","v","<",">"]
    self.state = [0, 0]
    self.goal = goal
    self.obstacle_reward = -1
    self.goal_reward = 1
    self.alive_reward = -0.1
    self.unavailable_reward = -1

    if goal==None:
      self.goal = [self.width-1, self.height-1]
    self.state += self.goal

    self._obstacles = []
    self.obstacles = []

    self.action_size = 5
    self.state_size = 4

  def reset(self):
    self.matrix = [["#" for j in range(self.width)] for i in range(self.height)]
    self.state = [0, 0] + self.goal
    self.obstacles = [obs for obs in self._obstacles]

    for obs in self.obstacles:
      if obs[4]:
        self.state += [obs[0]-self.state[0],obs[1]-self.state[1], obs[2]]

    return self.state

  def show(self, state, reward, action):
    clear_output()
    print(f"state:{state}, reward:{reward}, action:{self.act_to_str[action]}")
    print("-"+"-"*self.width*2+"-")

    for l in range(self.height):
      print("|", end="")
      for m in range(self.width):
        if self.state[0] == m and self.state[1] == l:
          print("A", end=" ")
        elif self.goal[0] == m and self.goal[1] == l:
          print("G", end=" ")
        else:
          print(self.matrix[l][m], end=" ")
      print("|")

    print("-"+"-"*self.width*2+"-")
    time.sleep(1)

  def add_obstacles(self, posx, posy, dir, act="", include_state=True): # 정지:O 상:^ 하:v 좌:< 우:> #method: "reflect", ["O","^","v","<",">"]
    self._obstacles.append([posx, posy, dir, act, include_state])
    self.state_size += 3 if include_state else 0

  def step(self, action, show=False):
    self.matrix = [["#" for j in range(self.width)] for i in range(self.height)]

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
      else:
        obs[2] = obs[3][random.randrange(0, len(obs[3]))]
      #matrix에 추가
      self.matrix[obs[1]][obs[0]] = self.act_to_str[obs[2]]


    # 에이전트 움직이기
    next = [self.state[0],self.state[1]]
    reward = 0
    done = False

    if action == 0:
      next = next
    elif action == 1 and not self.state[1]==0:
      next[1] -= 1
    elif action == 2 and not self.state[1]==self.height-1:
      next[1] += 1
    elif action == 3 and not self.state[0]==0:
      next[0] -= 1
    elif action == 4 and not self.state[0]==self.width-1:
      next[0] += 1
    else:
      next = next
      reward += self.unavailable_reward

    #보상, 완료 여부

    next += [self.goal[0]-next[0], self.goal[1]-next[1]]

    if self.matrix[next[1]][next[0]] in self.act_to_str:
      reward += self.obstacle_reward
      done = True
    elif next[0]==self.goal[0] and next[1]==self.goal[1]:
      reward += self.goal_reward
      done = True
    else:
      pass
    reward += self.alive_reward

    for obs in self.obstacles:
      if obs[4]:
        next += [obs[0]-self.state[0],obs[1]-self.state[1], obs[2]]

    self.state = next

    if show:
      env.show(next, reward, action)

    return self.state, reward, done
