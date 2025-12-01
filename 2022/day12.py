import sys
sys.path.append('.')
import aoc
import math
from aoc_utils.grid import *

data_rows = aoc.get_input(12, sample=False, index=0).splitlines()

def parse_input(rows):
  tmp = []
  start_coord = None
  target_coord = None
  for i,row in enumerate(rows):
    tmp_row = []
    for j,c in enumerate(row):
      if c == "S":
        start_coord = Coord(i, j)
        tmp_row.append(0)
      elif c == "E":
        target_coord = Coord(i, j)
        tmp_row.append(25)
      else:
        tmp_row.append(ord(c) - ord('a'))
    tmp.append(tmp_row)
  # tmp[1][0] = 5
  grid = Grid(tmp)
  return grid, start_coord, target_coord

def print_grid(grid, start, end):
  s = ""
  for i,row in enumerate(grid.numpy()):
    row_s = ""
    for j, val in enumerate(row):
      c = chr(val + ord('a'))
      if start == Coord(i,j):
        c = "S"
      if end == Coord(i,j):
        c= "E"
      row_s += c
    s += row_s + "\n"
  print(s)


def part1():
  grid, start, target = parse_input(data_rows)
  # print(grid.numpy())
  # print(start)
  # print(target)
  # print_grid(grid, start, target)

  def neighbor_fn(grid, cur_coord):
    rtn = []
    height = grid.safe_get(cur_coord)
    neighbors = grid.get_neighbors(cur_coord)
    for n_coord, n_height in neighbors:
      if n_height - height <= 1:
        n_cost = 1
        rtn.append((n_coord, n_cost))

    return rtn

  cost, path = find_path(start, target, grid, neighbor_fn=neighbor_fn)
  # print(cost)
  # print(path)
#   print(len(path)-1)

# part1()

def part2():
  grid, _, target = parse_input(data_rows)
  all_a_coords = np.nonzero(grid.numpy() == 0)
  all_a_coords = [Coord(all_a_coords[0][i],all_a_coords[1][i]) for i in range(all_a_coords[0].shape[0])]
  print(all_a_coords)

  def neighbor_fn(grid, cur_coord):
    rtn = []
    height = grid.safe_get(cur_coord)
    neighbors = grid.get_neighbors(cur_coord)
    for n_coord, n_height in neighbors:
      if n_height - height <= 1:
        n_cost = 1
        rtn.append((n_coord, n_cost))
    return rtn

  best_path = 10000000
  for start in all_a_coords:
    cost, path = find_path(start, target, grid, neighbor_fn=neighbor_fn)  
    print(f"For start {start}, cost: {cost}")
    if path and len(path) < best_path:
      best_path = len(path) - 1
  print(best_path)
  

part2()