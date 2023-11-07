import gym
from gym import spaces
import random
import numpy as np
import os
from itertools import combinations

class YachtDice(gym.Env):
    def __init__(self):
        self.boardname = ['Aces\t', 'Deuces', 'Threes', 'Fours', 'Fives', 'Sixes', 'Choice'
                          , '4 of a Kind', 'Full House', 'S. Straight', 'L. Straight', 'Yacht']
        self.action_size = 17
        self.state_size = 23
        self.panelty = -1
        self.reset()

    def get_possible_actions(self):
        actions = []
        for i in range(12):
            a = self.get_dummy_action()
            a[i] = 1
            actions.append(a)
        def index_combinations(lst):
            n = len(lst)
            for r in range(1, n + 1):
                for combo in combinations(range(n), r):
                    yield combo
        for combo in index_combinations(list(range(5))):
            a = self.get_dummy_action()
            for i in range(12, 17):
                if i - 12 in combo:
                    a[i] = 1
            actions.append(a)
        return actions

    def get_dummy_action(self):
        return [0] * 12 + [0] * 5

    def step(self, action):
        place = action[:12]
        save = action[12:]

        save_idx = []
        save_idx_count = 0

        reward = 0

        done = False

        for r in save: # save idx
            if r > 0.5:
                save_idx.append(save_idx_count)
            save_idx_count += 1
        
        if self.rollcount > 0:
            passed = True
            for idx in save_idx: # is this already saved?
                if self.hand_mask[idx] == 1:
                    passed = False
                    break
            if passed:
                # print(save_idx)
                for idx in save_idx:
                    self.hand_mask[idx] = 1 # save the dices

                passed = True
                for idx in range(5): # if all dices masked?
                    if self.hand_mask[idx] != 1:
                        passed = False
                        break 
                if passed: # all dices has saved
                    # print('all dices masked')
                    self.rollcount = 0
                else:
                    roll_idx = []
                    for i in range(5):
                        if self.hand_mask[i] == -1:
                            roll_idx.append(i)
                    # print(roll_idx)
                    self.roll(roll_idx)

                    return self._get_obs(), reward, done, []
            else:
                # print('Invalid Action : This dices are already saved.')
                reward += self.panelty

        passed = False
        for i in place: # Valid Place idx?
            if i != 0:
                passed = True
                break
        if not passed:
            # print('Invalid Action : No Place idx.')
            reward += self.panelty
        else:
            place_idx = np.argmax(place) # place idx
            if self.scoreboard[place_idx] == -1: # is this already placed?
                self.scoreboard[place_idx] = self.calculate_score(place_idx)
                self.turncount += 1
                self.rollcount = 3
                self.hand_mask = [-1] * 5
                self.roll(list(range(5)))
            else:
                # print('Invalid Action : That already placed.')
                reward += self.panelty

            if self.turncount == len(self.scoreboard) + 1:
                reward += np.sum(np.array(self.scoreboard)) / 500
                done = True

        return self._get_obs(), reward, done, []

    def reset(self):
        self.scoreboard = [-1] * 12
        self.hand = [-1] * 5
        self.hand_mask = [-1] * 5
        self.rollcount = 3
        self.turncount = 1
        self.roll(list(range(5)))

        return self._get_obs()

    def render(self):
        os.system('cls')
        self._show_board()

    def _get_obs(self):
        state = self.scoreboard+self.hand+self.hand_mask+[self.rollcount]
        return state

    def roll(self, idx):
        if self.rollcount > 0:
            for i in idx:
                self.hand[i] = random.randint(1, 6)
            self.rollcount -= 1
            if self.rollcount == 0:
                self.hand_mask = [1] * 5

    def _show_board(self):
        print('Yacht Dice by jellyho')
        print(f'TURN : {self.turncount}')
        print("=====================================")
        for i in range(6):
            print(f"{i+1}. {self.boardname[i]}\t\t{'-' if self.scoreboard[i] == -1 else self.scoreboard[i]}")
        print("-------------------------------------")
        for i in range(6, 12):
            print(f"{i+1}. {self.boardname[i]}\t\t{'-' if self.scoreboard[i] == -1 else self.scoreboard[i]}")
        print("-------------------------------------")
        mask = [str(i+1) if self.hand_mask[i] == -1 else '-' for i in range(5)]
        hand_mask = ''
        for m in mask:
            hand_mask += m + '  '
        print(f"`````````{hand_mask[:-2]}```````````````")
        print('Dice : ', self.hand, '   Reroll:', self.rollcount)
        print("=====================================")
        print()

    def calculate_score(self, i):
        dices = np.array(self.hand)
        if i in list(range(6)): #Aces ~ Sixes
            return np.sum(dices[np.where(dices==i+1)])
        elif i == 6: # Choice
            return np.sum(dices)
        elif i == 7: # 4 of a Kind
            for i in range(1, 7):
                if len(np.where(dices==i)) >= 4:
                    return np.sum(dices)
            return 0
        elif i == 8: # Full House
            self.hand.sort()
            lst = self.hand
            counts = {}
            for num in lst:
                if num in counts:
                    counts[num] += 1
                else:
                    counts[num] = 1
            if len(counts) == 2 and 3 in counts.values():
                return np.sum(dices)
            return 0
        elif i == 9: # S Staright
            self.hand.sort()
            sorted = self.hand
            count = [0] * 6
            for s in sorted:
                count[s-1] += 1
            for i in range(2):
                passed = True
                for j in range(3):
                    if count[i + j] > 0 and count[i + j + 1] > 0:
                        continue
                    else:
                        passed = False
                        break
                if passed:
                    return 15
            return 0
        elif i == 10: # L Straight
            self.hand.sort()
            sorted = self.hand
            for h in range(4):
                if sorted[h] + 1 != sorted[h + 1]:
                    return 0
            return 30
        elif i == 11: # Yacht
            for h in range(1, 7):
                if len(np.where(dices==h)) == 5:
                    return 50
            return 0

        
if __name__ == "__main__":
    env = YachtDice()
    state = env.reset()
    done = False

    while not done:
        env.render()
        
        action = env.get_dummy_action()

        if state[-1] != 0:
            idx = input('input save indexes (1 ~ 5) : ').split(' ')
            if idx != '':
                for i in range(5):
                    if str(i+1) in idx:
                        action[int(i) + 12] = 1
                state, reward, done, _ = env.step(action)
                continue
        place = int(input('input index of space that you want to place : '))
        action[place-1] = 1
        state, reward, done, _ = env.step(action)
    env.render()
    print("Game Finished, Total Score is ", reward * 500)