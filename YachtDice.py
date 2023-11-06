import gym
from gym import spaces
import random
import numpy as np

class YachtDice(gym.Env):
    def __init__(self):
        self.reset()

    def _step(self, action):
        place = action[:11]
        roll = action[11:]
        roll_idx = []
        roll_idx_count = 0

        for r in roll:
            if r > 0.5:
                roll_idx.append(roll_idx_count)
            roll_idx_count += 1
        
        if len(roll_idx) > 0:
            self.roll(roll_idx)
        else:
            place_idx = np.argmax(place)
            self.scoreboard[place_idx] = self.calculate_score[place_idx]

        return None

    def reset(self):
        self.scoreboard = [-1] * 11
        self.hand = [-1] * 5
        self.rollcount = 3
        self.roll(list(range(5)))

        return self._get_obs()

    def _render(self):
        self._show_board()

    def _get_obs(self):
        state = self.scoreboard+self.hand+[self.rollcount]
        return state

    def roll(self, idx):
        if self.rollcount > 0:
            for i in idx:
                self.hand[i] = random.randint(1, 6)
            self.rollcount -= 1

    def _show_board(self):
        pass

    def calculate_score(self, i):
        dices = np.array(self.hand)
        if i in list(range(6)): #Aces~Sixes
            return np.sum(dices[np.where(dices==i)])
        
if __name__ == "__main__":
    env = YachtDice()
    obs = env.reset()
    print(obs)
    print(env.calculate_score(3))
