from agents import QLearning
from YachtDice import YachtDice
import numpy as np

env = YachtDice()
actions = env.get_possible_actions()
agent = QLearning(actions)

ep = 1000000

mean = 0

for e in range(ep):
    state = env.reset()
    done = False
    rewards = 0
    while not done:
        if e % 1000 == 0:
            env.render()
        
        action = agent.get_action(state)
        next_state, reward, done, _ = env.step(action)

        agent.learn(state, action, reward, next_state)

        state = next_state
        rewards += reward

    mean = reward * 0.1 + mean * 0.9

    if e % 1000 == 0:
        env.render()
        agent.save('qlist.csv')
        print(f'\r{e}\t{mean}    ', end='')