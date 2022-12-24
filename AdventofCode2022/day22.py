import sys
sys.path.append('.')
import aoc
import math
import numpy as np
import enum
from aoc_utils.parsing import group_by_blank_lines

data_rows = aoc.get_input(22, sample=False, index=0).splitlines()

INVALID = 0
FREE = 1
BLOCKED = 2

class NonSquareGridWithWrapping:
  def __init__(self, data_rows):
    # Find max width of grid
    self.x_max = 0
    self.y_max = len(data_rows)
    for row in data_rows:
      self.x_max = max(len(row), self.x_max)

    # Populate grid
    self.data = np.zeros((self.y_max, self.x_max), dtype=int)
    for row_ix, row in enumerate(data_rows):
      for col_ix, c in enumerate(row):
        if c == " ":
          continue
        if c == ".":
          self.data[row_ix, col_ix] = FREE
        if c == "#":
          self.data[row_ix, col_ix] = BLOCKED

    # Find wrapping edges
    self.y_wraps = {}
    for y in range(self.y_max):
      first_valid = None
      last_valid = None
      for x in range(self.x_max):
        v = self.get_xy((x,y))
        if first_valid is None and v != INVALID:
          first_valid = x
        if first_valid is not None and v == INVALID:
          last_valid = x-1
          break
      if last_valid is None:
        last_valid = x
      self.y_wraps[y] = (first_valid, last_valid)
    self.x_wraps = {}
    for x in range(self.x_max):
      first_valid = None
      last_valid = None
      for y in range(self.y_max):
        v = self.get_xy((x,y))
        if first_valid is None and v != INVALID:
          first_valid = y
        if first_valid is not None and v == INVALID:
          last_valid = y-1
          break
      if last_valid is None:
        last_valid = y
      self.x_wraps[x] = (first_valid, last_valid)

  def get_xy(self, xy):
    x = xy[0]
    y = self.y_max - xy[1] - 1
    try:
      val = self.data[y, x]
    except IndexError:
      return INVALID
    # print(f"get {xy}: {val} (data index: {x},{y})")
    return val

  def _in_bounds(self, xy):
    if np.any(xy < np.asarray([0,0], dtype=int)) or np.any(xy > np.asarray([self.x_max, self.y_max], dtype=int)):
      return False
    return True

  def _wrap_val(self, xy, dir):
    wrap_xy = None
    if np.abs(dir[0]) > 0:
      # If moving in x dir
      wrap_vals = self.y_wraps[xy[1]]
      if wrap_vals[0] == xy[0]:
        wrapped_val = wrap_vals[1]
      elif wrap_vals[1] == xy[0]:
        wrapped_val = wrap_vals[0]
      else:
        raise ValueError(f"Did not find edge val {xy[0]} in wrap vals {wrap_vals}")
      wrap_xy = np.asarray([wrapped_val, xy[1]], dtype=int)
    else:
      # If moving in y dir
      wrap_vals = self.x_wraps[xy[0]]
      if wrap_vals[0] == xy[1]:
        wrapped_val = wrap_vals[1]
      elif wrap_vals[1] == xy[1]:
        wrapped_val = wrap_vals[0]
      else:
        raise ValueError(f"Did not find edge val {xy[1]} in wrap vals {wrap_vals}")
      wrap_xy = np.asarray([xy[0], wrapped_val], dtype=int)
    return wrap_xy

  def step(self, xy, dir):
    new_xy = xy + dir
    wrap = False
    new_val = new_xy
    stopped = False
    if self._in_bounds(new_xy):
      val = self.get_xy(new_xy)
      if val == INVALID:
        wrap = True
      elif val == BLOCKED:
        new_val = xy
        stopped = True
    else:
      wrap = True

    if wrap:
      wrap_xy = self._wrap_val(xy, dir)
      val = self.get_xy(wrap_xy)
      if val == INVALID:
        raise ValueError(f"Invalid wrapping")
      elif val == BLOCKED:
        new_val = xy
        stopped = True
      else:
        new_val = wrap_xy

    return (new_val, stopped)
        
def parse_steps(step_rows):
  steps = []
  active = ""
  for c in step_rows[0]:
    if c == "R":
      if len(active) > 0:
        steps.append(int(active))
        active = ""
      steps.append("R")
    elif c == "L":
      if len(active) > 0:
        steps.append(int(active))
        active = ""
      steps.append("L")
    else:
      active += c
  if len(active) > 0:
    steps.append(int(active))
  return steps

def rotate(dir, step):
  dirs = [np.asarray([1,0], dtype=int),
         np.asarray([0,-1], dtype=int), 
         np.asarray([-1, 0], dtype=int),
         np.asarray([0,1], dtype=int)]
  ix = None
  for i,d in enumerate(dirs):
    if np.all(dir == d):
      ix = i
      break
  if step == "L":
    ix -= 1
  else:
    ix += 1

  ix = ix % 4
  return dirs[ix]


def do_step(xy, dir, grid, step):
  if step == "L" or step == "R":
    dir = rotate(dir, step)
  else:
    for i in range(step):
      xy, stopped = grid.step(xy, dir)
      if stopped:
        break
  return xy, dir

def to_pass(xy, dir, y_max):
  col = xy[0] + 1
  row = y_max - xy[1]
  dir_mapping = {(1,0): 0, (0,-1): 1, (-1,0): 2, (0,1): 3}
  dir_val = dir_mapping[tuple(dir)]
  print(f"col: {col}, row: {row}, dir: {dir_val}")
  return 1000 * row + 4 * col + dir_val


def part1():
  grid_rows, step_rows = group_by_blank_lines(data_rows)
  grid = NonSquareGridWithWrapping(grid_rows)
  steps = parse_steps(step_rows)

  start_y = grid.y_max - 1
  start_x = 0
  while grid.get_xy((start_x, start_y)) == INVALID:
    start_x += 1

  xy = np.asarray([start_x, start_y], dtype=int)
  dir = np.asarray([1,0], dtype=int)
  # print(f"at {xy}, facing {dir}")
  for step in steps:
    xy, dir = do_step(xy, dir, grid, step)
    # print(f"at {xy}, facing {dir}")
  print(to_pass(xy, dir, grid.y_max))

part1()

#def part2():
#  pass

#part2()