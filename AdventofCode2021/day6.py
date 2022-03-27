import sys
sys.path.append('.')
import aoc

data_rows = aoc.get_input(6, sample=False).splitlines()

def step(timers):
    zeros = timers[0]
    for i in range(1,9):
        timers[i-1] = timers[i]
    timers[6] += zeros
    timers[8] = zeros

def part1():
    timers = { n:0 for n in range(9)}
    for val in data_rows[0].split(','):
        timers[int(val)] += 1

    for i in range(256):
        step(timers)

    total = 0
    for v in timers.values():
        total += v
    print(total)

part1()
