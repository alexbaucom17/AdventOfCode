import sys
sys.path.append('.')
import aoc
import math
import enum
from aoc_utils.grid import Point, ExpandingGrid
import numpy as np
import copy

data_rows = aoc.get_input(17, sample=False, index=0).splitlines()

class RockShape(enum.Enum):
  H_LINE = 0,
  PLUS = 1,
  L = 2,
  V_LINE = 3,
  SQUARE = 4

def get_shape(shape: RockShape):
  if shape == RockShape.H_LINE:
    return np.asarray(
      [[0,0],
       [1,0],
       [2,0],
       [3,0]],
       dtype=int
    )
  if shape == RockShape.PLUS:
    return np.asarray(
      [[0,1],
       [1,1],
       [2,1],
       [1,0],
       [1,2]],
       dtype=int
    )
  if shape == RockShape.L:
    return np.asarray(
      [[0,0],
       [1,0],
       [2,0],
       [2,1],
       [2,2]],
       dtype=int
    )
  if shape == RockShape.V_LINE:
    return np.asarray(
      [[0,0],
       [0,1],
       [0,2],
       [0,3]],
       dtype=int
    )
  if shape == RockShape.SQUARE:
    return np.asarray(
      [[0,0],
       [0,1],
       [1,1],
       [1,0]],
       dtype=int
    )

class RockSim:

  def __init__(self, wind: list[str]):
    self.wind = wind
    self.wind_ix = 0
    self.wind_dir = {">": np.asarray([1,0], dtype=int), "<": np.asarray([-1,0], dtype=int)}
    self.rock_order = [RockShape.H_LINE, RockShape.PLUS, RockShape.L, RockShape.V_LINE, RockShape.SQUARE]
    self.rock_ix = 0
    self.grid = ExpandingGrid(init_offset_x=0, init_offset_y=0, default_val=False)
    self.grid.set(Point(6,6), False)

    self.active_points = None
    self.insert_point = np.asarray([2, 3], dtype=int)

  def full_fall(self):
    self.active_points = get_shape(self.rock_order[self.rock_ix])
    self.active_points += self.insert_point

    while self.active_points is not None:
      # self.draw_active()
      self.push()
      self.fall()
    self.rock_ix = (self.rock_ix + 1) % len(self.rock_order)
    max_row = self.get_highest_row()
    self.insert_point = np.asarray([2, max_row+4], dtype=int)
    self.grid.set(Point(self.insert_point[0], self.insert_point[1]+5), False)

  def push(self):
    push_dir = self.wind_dir[self.wind[self.wind_ix]]
    self.wind_ix = (self.wind_ix + 1) % len(self.wind)
    new_points = self.active_points + push_dir
    obstacle = False
    for p in new_points:
      obstacle |= self.grid.get_oob(Point(p[0], p[1]), True)

    if not obstacle:
      self.active_points = new_points

  def fall(self):
    new_points = self.active_points + np.asarray([0, -1], dtype=int)
    obstacle = False
    for p in new_points:
      obstacle |= self.grid.get_oob(Point(p[0], p[1]), True)

    if obstacle:
      for p in self.active_points:
        self.grid.set(Point(p[0], p[1]), True)
      self.active_points = None
    else:
      self.active_points = new_points

  def get_highest_row(self):
    x_lims = self.grid.x_lims()
    y_lims = self.grid.y_lims()
    for y in range(y_lims[1], y_lims[0], -1):
      for x in range(x_lims[0], x_lims[1]):
        if self.grid.get(Point(x,y)):
          return y
    return y_lims[0]

  def find_full_rows(self):
    x_lims = self.grid.x_lims()
    y_lims = self.grid.y_lims()
    full_rows = []
    for y in range(y_lims[1], y_lims[0], -1):
      full_row = True
      for x in range(x_lims[0], x_lims[1]):
        full_row &= self.grid.get(Point(x,y))
      if full_row:
        full_rows.append(y)
    return full_rows

  def draw_active(self):
    tmp_grid = copy.deepcopy(self.grid)
    for p in self.active_points:
      tmp_grid.set(Point(p[0], p[1]), True)

    s = ""
    for row in reversed(tmp_grid.data):
      for c in row:
        s += "#" if c else "."
      s += "\n"
    print(s)

  def draw(self):
    s = ""
    for row in reversed(self.grid.data):
      for c in row:
        s += "#" if c else "."
      s += "\n"
    print(s)

def part1():
  wind = data_rows[0]
  sim = RockSim(wind)
  for i in range(2022):
    sim.full_fall()
    # sim.draw()
    # print("----------------------------------------")
  print(sim.get_highest_row()+1)
  print(sim.find_full_rows())

part1()

#def part2():
#  pass

#part2()