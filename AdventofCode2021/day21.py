import sys

from numpy import roll
sys.path.append('.')
import aoc
import math
import queue
from dataclasses import dataclass
from collections import defaultdict

class Die:

    def __init__(self):
        self.roll_count = 0

    def roll(self):
        self.roll_count += 1
        return -1

class DeterministicDie(Die):

    def __init__(self):
        super().__init__()
        self.die_value = 0

    def roll(self):
        super().roll()
        self.die_value += 1
        if self.die_value > 100:
            self.die_value = 1
        return self.die_value

class Player:

    def __init__(self, id, start):
        self.id = id
        self.value = start
        self.score = 0

    def turn(self, die: Die):
        rolls = die.roll() + die.roll() + die.roll()
        self.turn_from_sum(rolls)

    def turn_from_sum(self, sum):
        self.value = (self.value + sum) % 10
        if self.value == 0:
            self.score += 10
        else:
            self.score += self.value

    def __str__(self):
        return f"Player {self.id} - Score: {self.score}, Value: {self.value}"

def part1():
    sample = True
    p1_start = 6
    p2_start = 2
    if sample:
        p1_start = 4
        p2_start = 8
    die = DeterministicDie()
    p1 = Player("1", p1_start)
    p2 = Player("2", p2_start)

    winner = None
    loser = None
    while True:
        p1.turn(die)
        # print(p1)
        if p1.score >= 1000:
            winner = p1
            loser = p2
            break
        p2.turn(die)
        # print(p2)
        if p2.score >= 1000:
            winner = p2
            loser = p1
            break

    print(f"Winner: {str(winner)}")
    print(f"Answer: {loser.score * die.roll_count}")
# part1()


# @dataclass(frozen=True)
# class PlayerData:
#     value: int
#     score: int
#     id: int

#     def turn_from_sum(self, sum):
#         new_value = (self.value + sum) % 10
#         if new_value == 0:
#             new_score = self.score + 10
#         else:
#             new_score = self.score + self.value
#         return PlayerData(new_value, new_score, self.id)

# def score_full_die_pattern(p1_start, p2_start, rolls):
#     if len(rolls) % 3 != 0:
#         return (None, None, None, None)
#     n_turns = int(len(rolls) / 3)

#     p1 = PlayerData(p1_start, 0, 1)
#     p2 = PlayerData(p2_start, 0, 2)
#     p1_turn = True
#     winner = None
#     loser = None
#     end_score = 19

#     for i in range(n_turns):
#         sum_rolls = sum(rolls[3*i:3*i+3])
#         if p1_turn:
#             p1 = p1.turn_from_sum(sum_rolls)
#             p1_turn = False
#             if p1.score >= end_score:
#                 winner = p1
#                 loser = p2
#                 break
#         else:
#             p2 = p2.turn_from_sum(sum_rolls)
#             p1_turn = True
#             if p2.score >= end_score:
#                 winner = p2
#                 loser = p1
#                 break
#     return (p1, p2, winner, loser)


# @dataclass
# class QueueElement:
#     p1: PlayerData
#     p2: PlayerData
#     p1_turn: bool
#     prev_rolls: list[int]
#     new_rolls: list[int]

# def score_queue_element(elem: QueueElement, end_score: int):
#     sum_rolls = sum(elem.new_rolls)
#     p1 = elem.p1
#     p2 = elem.p2
#     winner = None
#     if elem.p1_turn:
#         p1 = p1.turn_from_sum(sum_rolls)
#         if p1.score >= end_score:
#             winner = p1
#     else:
#         p2 = p2.turn_from_sum(sum_rolls)
#         if p2.score >= end_score:
#             winner = p2
#     return (p1, p2, winner)

# def part2():

#     sample = True
#     p1_start = 6
#     p2_start = 2
#     if sample:
#         p1_start = 4
#         p2_start = 8
#     end_score = 21

#     q = queue.LifoQueue()
#     p1 = PlayerData(p1_start, 0, 1)
#     p2 = PlayerData(p2_start, 0, 2)
#     p1_win_count = 0
#     p2_win_count = 0
#     q.put(QueueElement(p1, p2, True, [], [1]))
#     q.put(QueueElement(p1, p2, True, [], [2]))
#     q.put(QueueElement(p1, p2, True, [], [3]))

#     while not q.empty():
#         elem = q.get()
#         if len(elem.new_rolls) == 3:
#             p1, p2, winner = score_queue_element(elem, end_score)
#             if winner is not None:
#                 if winner.id == 1:
#                     p1_win_count += 1
#                     if p1_win_count % 1000000 == 0:
#                         print(p1_win_count)
#                 else:
#                     p2_win_count += 1
#                 continue
#             else:
#                 for i in [1,2,3]:
#                     q.put(QueueElement(
#                         p1,
#                         p2,
#                         not elem.p1_turn,
#                         elem.prev_rolls + elem.new_rolls,
#                         [i]
#                     ))
#         else:
#             for i in [1,2,3]:
#                 q.put(QueueElement(
#                     elem.p1,
#                     elem.p2,
#                     elem.p1_turn,
#                     elem.prev_rolls,
#                     elem.new_rolls + [i]
#                 ))
#             continue

#     print(f"P1 win count: {p1_win_count}")
#     print(f"P2 win count: {p2_win_count}")
# part2()

            
def make_sums():
    sums = defaultdict(int)
    for i in [1,2,3]:
        for j in [1,2,3]:
            for k in [1,2,3]:
                sums[i+j+k] += 1
    return sums

class QuantumPlayer:
    def __init__(self, id, starting_val):
        self.data = {i:None for i in range(10)}
        self.data[starting_val] = {0: 1}
        self.id = id

    def turn(self, sum_dict, end_score):
        new_data = {i:None for i in range(10)}
        num_wins = 0
        for value, score_dict in self.data.items():
            if score_dict is None:
                continue
            for cur_sum, sum_count in sum_dict.items():
                new_value = (value + cur_sum) % 10
                score_change = new_value if new_value != 0 else 10
                new_score_dict = {}
                for score, score_count in score_dict.items():
                    new_score = score + score_change
                    new_count = score_count * sum_count
                    if new_score >= end_score:
                        num_wins += new_count
                    else:
                        new_score_dict[new_score] = new_count
                if new_data[new_value] is None:
                    new_data[new_value] = new_score_dict
                else:
                    merged = {i: new_data[new_value].get(i, 0) + new_score_dict.get(i, 0) for i in set(new_data[new_value]) | set(new_score_dict)}
                    new_data[new_value] = merged
        self.data = new_data
        return num_wins

    def expand_futures(self, num):
        new_data = {}
        for k, score_dict in self.data.items():
            if score_dict:
                score_dict = {k:num*v for k,v in score_dict.items()}
            new_data[k] = score_dict
        self.data = new_data

    def __str__(self):
        s = f"Player {self.id}: \n"
        for k, v in self.data.items():
            s += f"{k}: {str(v)}\n"
        return s

    def empty(self):
        for v in self.data.values():
            if v:
                return False
        return True


def part2():
    sample = True
    p1_start = 6
    p2_start = 2
    if sample:
        p1_start = 4
        p2_start = 8
    end_score = 21
    iters = 10000
    roll_sums = make_sums()
    print(roll_sums)

    p1 = QuantumPlayer(1, p1_start)       
    p2 = QuantumPlayer(2, p2_start)
    p1_wins = 0
    p2_wins = 0
    print(p1)
    print(p2)

    for i in range(iters):
        p1_wins += p1.turn(roll_sums, end_score)
        p2.expand_futures(27)
        p2_wins += p2.turn(roll_sums, end_score)
        p1.expand_futures(27)

        if i < 10:
            print(i)
            print(p1)
            print(p2)

        if p1.empty() or p2.empty():
            print(f"Complete: {i}")
            break



    print(p1)
    print(p2)
    print(f"p1 wins: {p1_wins}, p2 wins: {p2_wins}")

part2()


