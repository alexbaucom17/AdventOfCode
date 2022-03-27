import sys
sys.path.append('.')
import aoc
import numpy as np

data_rows = aoc.get_input(7, sample=False).splitlines()
csum = np.cumsum(np.arange(1882))

def cost(crabs, target):
    return np.sum(np.abs(crabs-target))

def cost2(crabs, target):
    c_cost = csum[np.abs(crabs-target)]
    return np.sum(c_cost)


def part1():
    crabs = np.asarray([int(c) for c in data_rows[0].split(',')])
    cmin = np.min(crabs)
    cmax = np.max(crabs)
    print(cmin)
    print(cmax)
    best = 999999999
    best_ix = 99999999
    for p in range(cmin, cmax+1):
        fuel = cost2(crabs, p)
        if fuel < best:
            best = fuel
            best_ix = p

    print(f"Best pos is {best_ix} with {best} fuel")

part1()