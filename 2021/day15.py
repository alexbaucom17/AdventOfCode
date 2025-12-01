import sys
sys.path.append('.')
import aoc
import math 
import copy
from aoc_utils import grid, parsing

data_rows = aoc.get_input(15, sample=False).splitlines()

def part1():
    g = grid.Grid(parsing.int_grid(data_rows))
    start = grid.Coord(0,0)
    end = grid.Coord(g.n_rows-1, g.n_cols-1)
    cost, path = grid.find_path(start, end, g, cost_fn=grid.astar_cost_fn)
    # print(path)
    print(cost)
# part1()

def part2(): 
    g = parsing.int_grid(data_rows)
    g_rows = len(g)
    g_cols = len(g[0])
    uber_grid = [[0 for i in range(5*g_cols)] for j in range(5*g_rows)]
    for i in range(5):
        for j in range(5):
            for k in range(g_rows):
                for v in range(g_cols):
                    new_i = i*g_rows + k
                    new_j = j*g_cols + v
                    new_val = g[k][v] + i + j
                    if new_val > 9:
                        new_val -= 9
                    uber_grid[new_i][new_j] = new_val

    uber_grid = grid.Grid(uber_grid)
    # print(uber_grid)

    start = grid.Coord(0,0)
    end = grid.Coord(uber_grid.n_rows-1, uber_grid.n_cols-1)
    cost, _ = grid.find_path(start, end, uber_grid, cost_fn=grid.astar_cost_fn)
    print(cost)
part2()