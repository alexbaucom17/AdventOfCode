import sys

sys.path.append('.')
import aoc
import math
import queue
from dataclasses import dataclass, replace
from collections import defaultdict
import cProfile
from functools import cache


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

            
def make_sums():
    sums = defaultdict(int)
    for i in [1,2,3]:
        for j in [1,2,3]:
            for k in [1,2,3]:
                sums[i+j+k] += 1
    return sums
all_roll_sums = make_sums()

@dataclass(frozen=True)
class Gamedata:
    p1_state: int
    p1_score: int
    p2_state: int
    p2_score: int
    p1_turn: bool
    n_universes: int
    recurse_level: int

@dataclass
class Windata:
    p1: int
    p2: int

max_score = 18

def turn(state: int, score: int, roll_sum: int) -> tuple[int, int]:
    total = (state + roll_sum) % 10
    new_state = total if total != 0 else 10
    new_score = score + new_state
    return (new_state, new_score)

@cache
def recurse_game(gamedata: Gamedata) -> Windata:
    wins = Windata(0,0)
    new_recurse_level = gamedata.recurse_level + 1
    # if gamedata.recurse_level < 3:
    #     print(gamedata)
    for total, count in all_roll_sums.items():
        if gamedata.recurse_level < 1:
            print(f"Checking {total} with count {count}")

        new_universe_count = gamedata.n_universes*count
        if gamedata.p1_turn:
            new_state, new_score = turn(gamedata.p1_state, gamedata.p1_score, total)

            if new_score >= max_score:
                wins.p1 += new_universe_count
                continue

            new_data = Gamedata(new_state, new_score, gamedata.p2_state, gamedata.p2_score, False, 
                new_universe_count, new_recurse_level)
        else:
            new_state, new_score = turn(gamedata.p2_state, gamedata.p2_score, total)

            if new_score >= max_score:
                wins.p2 += new_universe_count
                continue

            new_data = Gamedata(gamedata.p1_state, gamedata.p1_score, new_state, new_score, True, 
                new_universe_count, new_recurse_level)
        
        new_wins = recurse_game(new_data)
        wins.p1 += new_wins.p1
        wins.p2 += new_wins.p2

    return wins

def part2():
    sample = False
    p1_start = 6
    p2_start = 2
    if sample:
        p1_start = 4
        p2_start = 8
    gamedata = Gamedata(p1_start, 0, p2_start, 0, True, 1, 0)
    print(recurse_game(gamedata))


# part2()

pr = cProfile.Profile()
pr.enable()
pr.run('part2()')
pr.disable()
import pstats
p = pstats.Stats(pr)
p.sort_stats(pstats.SortKey.TIME)
p.print_stats()



