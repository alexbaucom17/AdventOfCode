import sys
sys.path.append('.')
import aoc
import math
import numpy as np

data_rows = aoc.get_input(9, sample=False, index=1).splitlines()

def do_step(head, tail, step):
  new_head = head + step
  # print(f"new head: {new_head}")

  # Figure out new tail
  diff = new_head - tail
  abs_diff = np.abs(diff)
  bool_diff = abs_diff > 0
  # print(f"diffs: {diff}, {abs_diff}, {bool_diff}")
  # Axis touching case and stacked case
  if np.sum(abs_diff) < 2:
    # print("Axis touching/stacked")
    return (new_head, tail)
  
  # Diagonal case 
  if np.all(bool_diff):
    # Diagonal touching case
    if np.all(abs_diff == 1):
      # print("Diagonal touching")
      return (new_head, tail)
    else:
      # I think this works because the diff should always be +/-2 and +/-1 (unknown axes)
      # We need to align tail in the 2 direction, so floor(2/2)->1 and floor(1/2)->0
      tmp = np.around(diff/2).astype(int)
      new_tail = new_head - tmp
      # print(f"Diagonal update, tmp: {tmp}, new tail: {new_tail}")
      return (new_head, new_tail)
      
  # Axis aligned 2 steps case
  new_tail = new_head - np.around(diff/2).astype(int)
  # print(f"Axis update, new tail: {new_tail}")
  return (new_head, new_tail)

def show(head, tail, seen):
  grid = np.zeros((6,6), dtype=int)
  for s in seen:
    grid[s[1], s[0]] = 1
  grid[tail[1], tail[0]] = 2
  grid[head[1], head[0]] = 3
  print(np.flipud(grid))

def show2(points, seen, size=[6,6], offset=np.zeros((1,2), dtype=int)):
  grid = np.zeros(size, dtype=int)
  def coord(arr):
    return (arr[1] + offset[1], arr[0] + offset[0])
  for s in seen:
    grid[coord(s)] = -1
  for ix in range(points.shape[0]):
    p = points[ix, :]
    grid[coord(p)] = ix + 1
  print(np.flipud(grid))


def part1():
  head = np.asarray([0,0], dtype=int)
  tail = np.asarray([0,0], dtype=int)
  seen = set([tuple(tail)])
  for row in data_rows:
    dir, num = row.split()
    for i in range(int(num)):
      step = np.asarray([0,0], dtype=int)
      if dir == "U":
        step[1] = 1
      elif dir == "D":
        step[1] = -1
      elif dir == "L":
        step[0] = -1
      elif dir == "R":
        step[0] = 1
      else:
        raise ValueError(f"Invalid dir: {dir}")
      head, tail = do_step(head, tail, step)
      seen.add(tuple(tail))
      # show(head, tail, seen)

  print(len(seen))


# part1()

def step_from_command(dir, num):
  step = np.asarray([0,0], dtype=int)
  if dir == "U":
    step[1] = 1
  elif dir == "D":
    step[1] = -1
  elif dir == "L":
    step[0] = -1
  elif dir == "R":
    step[0] = 1
  else:
    raise ValueError(f"Invalid dir: {dir}")
  return step


def part2():
  points = np.zeros((10,2), dtype=int)
  seen = set([tuple(points[9, :])])
  for row in data_rows:
    dir, num = row.split()
    for i in range(int(num)):
      command_step = step_from_command(dir, num)
      points[0, :], points[1, :] = do_step(points[0,:], points[1,:], command_step)
      for j in range(1,9):
        points[j, :], points[j+1, :] = do_step(points[j,:], points[j+1,:], np.zeros_like(command_step))
      seen.add(tuple(points[9,:]))
      # print(seen)
    # show2(points, seen, size=[24,24], offset=np.asarray((7,7), dtype=int))
    # print("-----")
  print(len(seen))
        
     
part2()