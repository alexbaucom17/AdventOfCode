import sys
sys.path.append('.')
import aoc
from dataclasses import dataclass

data_rows = aoc.get_input(2, sample=False).splitlines()

@dataclass
class State: 
    depth: int
    pos: int
    aim: int

def step(state: State, dir: str, dist: int):
    if dir == 'forward':
        state.pos += dist
    elif dir == 'down':
        state.depth += dist
    elif dir == 'up':
        state.depth -= dist
    else:
        raise ValueError(f"Invalid dir: {dir}")

def step2(state: State, dir: str, dist: int):
    if dir == 'forward':
        state.pos += dist
        state.depth += state.aim * dist
    elif dir == 'down':
        state.aim += dist
    elif dir == 'up':
        state.aim -= dist
    else:
        raise ValueError(f"Invalid dir: {dir}")

def part1():
    state = State(0,0,0)
    for row in data_rows:
        dir, dist = row.split()
        step(state, dir, int(dist))
        # print(state)

    print(state.pos * state.depth)

part1()


def part2():
    state = State(0,0,0)
    for row in data_rows:
        dir, dist = row.split()
        step2(state, dir, int(dist))
        # print(state)

    print(state.pos * state.depth)

part2()

