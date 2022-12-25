import sys
sys.path.append('.')
import aoc
import math
import numpy as np
import time
import queue
import copy

data_rows = aoc.get_input(24, sample=False, index=1).splitlines()

char_map = {".": 0, ">": 1, "<": 2, "^": 3, "v": 4}
char_map_inv = {v:k for k,v in char_map.items()}
num_map_moves = {1: np.asarray([0, 1], dtype=int),
                 2: np.asarray([0, -1], dtype=int),
                 3: np.asarray([-1, 0], dtype=int),
                 4: np.asarray([1, 0], dtype=int)}

def parse_input(data_rows):
  start_loc = None
  end_loc = None
  n_grid_rows = len(data_rows) - 2
  n_grid_cols = len(data_rows[0]) - 2
  grid = np.zeros((n_grid_rows, n_grid_cols), dtype=int)
  for i, row in enumerate(data_rows):
    if i == 0:
      start_col = row.index(".") - 1
      start_loc = np.asarray([-1, start_col], dtype=int)
      continue
    if i == len(data_rows) - 1:
      end_col = row.index(".") - 1
      end_loc = np.asarray([n_grid_rows, end_col], dtype=int)
      continue
    for j, char in enumerate(row):
      if char == "#":
        continue
      grid[i-1, j-1] = char_map[char]
  return grid, start_loc, end_loc

def print_grid(grid):
  for row in grid:
    s = ""
    for num in row:
      if num > 4:
        s += str(len(str(num)))
      else:
        s += char_map_inv[num]
    print(s)

def encode(vals):
  # print(vals)
  if vals:
    return int("".join([str(v) for v in vals]))
  else:
    return 0

def decode(val):
  return [int(c) for c in str(val) if c != "0"]

def item_step(item, coord, grid):
  move = num_map_moves[item]
  new_coord = coord + move
  if new_coord[0] < 0:
    new_coord[0] = grid.shape[0] - 1
  elif new_coord[0] >= grid.shape[0]:
    new_coord[0] = 0
  elif new_coord[1] < 0:
    new_coord[1] = grid.shape[1] - 1
  elif new_coord[1] >= grid.shape[1]:
    new_coord[1] = 0
  return new_coord

def do_timestep(grid):
  out = np.zeros_like(grid)
  for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
      cur_items = decode(grid[i,j])
      # if cur_items:
        # print(f"Cur items at ({i}, {j}): {cur_items}")
      for item in cur_items:
        new_loc = item_step(item, np.asarray((i,j), dtype=int), grid)
        raw_val_new_loc = out[new_loc[0], new_loc[1]]
        # print(f"raw_val_new_loc: {raw_val_new_loc}")
        items_at_new_loc = decode(raw_val_new_loc)
        # print(f"new items decoded: {items_at_new_loc}")
        encoded_items = encode([item] + items_at_new_loc)
        # print(f"new items encoded: {encoded_items}")
        out[new_loc[0], new_loc[1]] = encoded_items
  # print(out)
  return out

def lcm(a, b):
  return int((a*b)/math.gcd(a,b))

def gen_3d_grid(grid):
  num_timesteps = lcm(grid.shape[0], grid.shape[1])
  data = np.zeros((grid.shape[0], grid.shape[1], num_timesteps), dtype=int)
  data[:, :, 0] = grid
  for ts in range(1, num_timesteps):
    # print(f"timestep: {ts}")
    data[:, :, ts] = do_timestep(data[:, :, ts-1])
  return data

def gen_next_vals(val, grid, target, start):
  adds = [
    np.asarray([0,0,1], dtype=int),
    np.asarray([1,0,1], dtype=int),
    np.asarray([-1,0,1], dtype=int),
    np.asarray([0,1,1], dtype=int),
    np.asarray([0,-1,1], dtype=int)
  ]
  new_vals = []
  for a in adds:
    candidate = val + a
    candidate[2] = candidate[2] % grid.shape[2]
    if candidate[0] < 0 or candidate[0] >= grid.shape[0] or candidate[1] < 0 or candidate[1] >= grid.shape[1]:
      if candidate[0] == target[0] and candidate[1] == target[1]:
        new_vals.append(candidate)
      elif candidate[0] == start[0] and candidate[1] == start[1]:
        new_vals.append(candidate)
      continue
    b = grid[candidate[0], candidate[1], candidate[2]]
    if b == 0:
      new_vals.append(candidate)
  return new_vals

def bfs_3d(grid, start, target, start_time=0):
  q = queue.Queue()
  start_time = start_time % grid.shape[2]
  q.put((np.asarray([start[0], start[1], start_time], dtype=int), 0))
  explored = set()

  while not q.empty():
    val, steps = q.get()
    # print(f"val: {val}, steps: {steps}")
    if val[0] == target[0] and val[1] == target[1]:
      return steps

    next_vals = gen_next_vals(val, grid, target, start)
    # print(next_vals)
    for val in next_vals:
      if tuple(val) in explored:
        continue
      else:
        explored.add(tuple(val))
        q.put((val, steps+1))

  return -1 

def part1():
  grid_2d, start, target = parse_input(data_rows)
  t_start = time.time()
  grid_3d = gen_3d_grid(grid_2d)
  print(f"Gen 3d grid with {grid_3d.shape[2]} steps in {time.time() - t_start:.4f} secs")
  t_start = time.time()
  # for i in range(grid_3d.shape[2]):
  #   print(i)
  #   print_grid(grid_3d[:, :, i])
  #   print("--------")
  steps = bfs_3d(grid_3d, start, target)
  print(f"Completed bfs in {time.time() - t_start:.4f} secs")
  print(steps)
  print(f"target: {target}")

# part1()

def part2():
  grid_2d, start, target = parse_input(data_rows)
  t_start = time.time()
  grid_3d = gen_3d_grid(grid_2d)
  print(f"Gen 3d grid with {grid_3d.shape[2]} steps in {time.time() - t_start:.4f} secs")
  t_start = time.time()

  steps_to_target = bfs_3d(grid_3d, start, target)
  print(f"steps to target: {steps_to_target}")

  steps_to_backtrack = bfs_3d(grid_3d, target, start, steps_to_target)
  print(f"steps_to_backtrack: {steps_to_backtrack}")

  steps_to_target2 = bfs_3d(grid_3d, start, target, steps_to_target + steps_to_backtrack)
  print(f"steps to target 2: {steps_to_target2}")
  
  print(f"Completed bfs in {time.time() - t_start:.4f} secs")
  print(steps_to_target + steps_to_backtrack + steps_to_target2)

part2()