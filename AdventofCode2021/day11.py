import sys
sys.path.append('.')
import aoc
import queue
from aoc_utils import grid

data_rows = aoc.get_input(11, sample=False).splitlines()
data_mat = [[int(i) for i in row] for row in data_rows]


def step(mat):
    to_flash = queue.Queue()
    has_flashed = set()
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            mat[i][j] += 1
            if mat[i][j] > 9:
                to_flash.put(grid.Coord(i,j))

    while not to_flash.empty():
        coord = to_flash.get()
        if coord in has_flashed:
            continue
        neighbors = grid.get_neighbors(coord, mat, neighbor_fn=grid.ortho_diag_neighbors)
        has_flashed.add(coord)
        # print(f"{coord}, {mat[coord.row][coord.col]}")
        # print(neighbors)
        for c, _ in neighbors:
            mat[c.row][c.col] += 1
            if mat[c.row][c.col] > 9 and c not in has_flashed:
                to_flash.put(c)
        # print(has_flashed)

    for c in has_flashed:
        mat[c.row][c.col] = 0

    return len(has_flashed)

def part1():
    total_flashes = 0
    for i in range(100):
        # for row in data_mat:
        #     print(row)
        cur_flashes = step(data_mat)
        # print(f"Cur flashes: {cur_flashes}")
        total_flashes += cur_flashes

    print(total_flashes)
            
# part1()

def part2():
    for i in range(1000):
        cur_flashes = step(data_mat)
        if cur_flashes == len(data_mat) * len(data_mat[0]):
            print(f"Flashes synced on step {i+1}")
            break

part2()