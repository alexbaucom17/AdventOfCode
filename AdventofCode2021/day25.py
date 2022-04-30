from shutil import move
import sys
from tabnanny import check
sys.path.append('.')
import aoc
import math
import numpy as np
from enum import Enum

data_rows = aoc.get_input(25, sample=False, index=0).splitlines()

class CType(Enum):
    NONE = 0,
    EAST = 1,
    SOUTH = 2

class SeaGrid:
    def __init__(self, data: list[list[int]]):
        self.data = np.asarray(data)
        self.east_locs = np.argwhere(self.data == CType.EAST)
        self.south_locs = np.argwhere(self.data == CType.SOUTH)
        self.east_step = np.repeat([[0,1]], self.east_locs.shape[0], axis=0)
        self.south_step = np.repeat([[1,0]], self.south_locs.shape[0], axis=0)

    def step_east(self):
        check_locs = self.east_locs + self.east_step
        check_locs[check_locs[:, 1] >= self.data.shape[1], 1] = 0
        empty_mask = self.data[check_locs[:,0], check_locs[:,1]] == CType.NONE
        old_locs = self.east_locs[empty_mask]
        move_locs = check_locs[empty_mask]
        self.data[old_locs[:, 0], old_locs[:, 1]] = CType.NONE
        self.data[move_locs[:, 0], move_locs[:, 1]] = CType.EAST
        self.east_locs[empty_mask] = move_locs
        return np.sum(empty_mask)

    def step_south(self):
        check_locs = self.south_locs + self.south_step
        check_locs[check_locs[:, 0] >= self.data.shape[0], 0] = 0
        empty_mask = self.data[check_locs[:,0], check_locs[:,1]] == CType.NONE
        old_locs = self.south_locs[empty_mask]
        move_locs = check_locs[empty_mask]
        self.data[old_locs[:, 0], old_locs[:, 1]] = CType.NONE
        self.data[move_locs[:, 0], move_locs[:, 1]] = CType.SOUTH
        self.south_locs[empty_mask] = move_locs
        return np.sum(empty_mask)
        
    def step(self):
        num_east = self.step_east()
        num_south = self.step_south()
        return num_east + num_south

    def __str__(self):
        out = ""
        for row in self.data:
            for val in row:
                if val == CType.NONE:
                    out += "."
                elif val == CType.EAST:
                    out += ">"
                elif val == CType.SOUTH:
                    out += "v"
            out += "\n"
        return out

def parse():
    grid_data = []
    for row in data_rows:
        row_data = []
        for c in row.strip():
            if c == '.':
                row_data.append(CType.NONE)
            elif c == '>':
                row_data.append(CType.EAST)
            elif c == 'v':
                row_data.append(CType.SOUTH)
            else:
                raise ValueError(f"Invalid char {c}")
        grid_data.append(row_data)
    return SeaGrid(grid_data)


def part1():
    g = parse()
    n_moved = 1
    count = 0
    while n_moved > 0:
        n_moved = g.step()
        count += 1

    print(count)

part1()


