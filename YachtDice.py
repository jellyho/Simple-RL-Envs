import gym
from gym import spaces
import random
import numpy as np

class YachtDice(gym.Env):
    def __init__(self):
        self.boardname = ['Aces\t', 'Deuces', 'Thress', 'Fours', 'Fives', 'Sixes', 'Choice'
                          , '4 of a Kind', 'Full House', 'S. Straight', 'L. Straight', 'Yacht']
        self.reset()

    def _step(self, action):
        place = action[:12]
        roll = action[12:]

        roll_idx = []
        roll_idx_count = 0

        reward = 0

        for r in roll:
            if r > 0.5:
                roll_idx.append(roll_idx_count)
            roll_idx_count += 1
        
        if len(roll_idx) > 0:
            if self.rollcount > 0:
                self.roll(roll_idx)
            else:
                pass
        else:
            place_idx = np.argmax(place)
            if self.scoreboard[place_idx] == -1:
                self.scoreboard[place_idx] = self.calculate_score[place_idx]
            else:
                pass

        return None

    def reset(self):
        self.scoreboard = [-1] * 12
        self.hand = [-1] * 5
        self.rollcount = 3
        self.turncount = 1
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
        print()
        print(f'TURN : {self.turncount}')
        print("=====================================")
        for i in range(12):
            print(f"{i}. {self.boardname[i]}\t\t{'-' if self.scoreboard[i] == -1 else self.scoreboard[i]}")
        print("-------------------------------------")
        print('Dice : ', self.hand, '   Reroll:', self.rollcount)
        print("=====================================")
        print()

    def calculate_score(self, i):
        dices = np.array(self.hand)
        if i in list(range(6)): #Aces ~ Sixes
            return np.sum(dices[np.where(dices==i)])
        elif i == 6: # Choice
            return np.sum(dices)
        elif i == 7: # 4 of a Kind
            pass
        
if __name__ == "__main__":
    env = YachtDice()
    obs = env.reset()
    print(obs)
    env._show_board()
