import sys
sys.path.append('.')
import aoc
import math
from aoc_utils.grid import Point
import copy
import enum
from aoc_utils.conversions import sign

data_rows = aoc.get_input(14, sample=False, index=0).splitlines()

class ExpandingGrid:
  def __init__(self, default_val=None):
    self.data = [[default_val for x in range(2)] for y in range(2)]
    self.x_offset = 495
    self.y_offset = 0
    self.default_val = default_val

  def x_lims(self):
    return (self.x_offset, self.x_offset + len(self.data[0]))

  def y_lims(self):
    return (self.y_offset, self.y_offset + len(self.data))

  def get(self, point: Point):
    if self._in_lims(point):
      return self.data[point.y-self.y_offset][point.x-self.x_offset] 
    else:
      return self.default_val

  def get_oob(self, point: Point, oob_val=None):
    if self._in_lims(point):
      return self.data[point.y-self.y_offset][point.x-self.x_offset] 
    else:
      return oob_val

  def _in_lims(self, point: Point):
    x_lims = self.x_lims()
    y_lims = self.y_lims()
    if point.y < y_lims[0] or point.y >= y_lims[1] or point.x < x_lims[0] or point.x >= x_lims[1]:
      return False
    else:
      return True
  
  def set(self, point: Point, val):
    if self._in_lims(point):
      self._fixed_set(point, val)
    else:
      self._expand_set(point, val)

  def _fixed_set(self, point: Point, val):
    # print("fixed set")
    y = point.y-self.y_offset
    x = point.x-self.x_offset
    # print(x)
    # print(y)
    self.data[y][x] = val

  def _expand_set(self, point: Point, val):
    cur_x_lim = self.x_lims()
    cur_y_lim = self.y_lims()
    new_x_lim = list(copy.deepcopy(cur_x_lim))
    new_y_lim = list(copy.deepcopy(cur_y_lim))
    if point.y < cur_y_lim[0]:
      new_y_lim[0] = point.y - 1
    if point.y >= cur_y_lim[1]:
      new_y_lim[1] = point.y + 1
    if point.x < cur_x_lim[0]:
      new_x_lim[0] = point.x - 1
    if point.x >= cur_x_lim[1]:
      new_x_lim[1] = point.x + 1

    # print("Expanding set")
    # print(cur_x_lim)
    # print(cur_y_lim)
    # print(new_x_lim)
    # print(new_y_lim)

    cur_dx = cur_x_lim[1] - cur_x_lim[0]
    cur_dy = cur_y_lim[1] - cur_y_lim[0]
    new_dx = new_x_lim[1] - new_x_lim[0]
    new_dy = new_y_lim[1] - new_y_lim[0]
    new_data = [[self.default_val for x in range(new_dx)] for y in range(new_dy)]
    new_to_cur_x = cur_x_lim[0] - new_x_lim[0]
    new_to_cur_y = cur_y_lim[0] - new_y_lim[0]
    # print(new_to_cur_x)
    # print(new_to_cur_y)
    # print(self.data)
    # print(new_data)
    for x in range(cur_dx):
      for y in range(cur_dy):
        new_data[new_to_cur_y + y][new_to_cur_x + x] = self.data[y][x]
    self.data = new_data
    
    self.x_offset = new_x_lim[0]
    self.y_offset = new_y_lim[0]
    # print(self.x_offset)
    # print(self.y_offset)
    self._fixed_set(point, val)


class Objects(enum.Enum):
  AIR = 0,
  ROCK = 1,
  SAND = 2,
  SAND_INIT = 3,
  TRACE = 4

class MoveStatus(enum.Enum):
  MOVED = 0,
  BLOCKED = 1,
  FIXED = 2,
  OOB = 3,
  AT_INIT = 4

char_map = {Objects.AIR: ".", Objects.ROCK: "#", Objects.SAND: "o", Objects.SAND_INIT: "+", Objects.TRACE: "~"}

class SandSim:
  def __init__(self, rock_paths, sand_init, use_floor=False):
    self.grid = ExpandingGrid(Objects.AIR)
    self.grid.set(sand_init, Objects.SAND_INIT)
    max_y = 0
    for path in rock_paths:
      for i in range(len(path) - 1):
        cur_x = path[i].x
        cur_y = path[i].y
        if cur_y > max_y:
          max_y = cur_y
        next_x = path[i+1].x
        next_y = path[i+1].y
        if next_y > max_y:
          max_y = next_y
        dx = next_x - cur_x 
        dy = next_y - cur_y
        if dx != 0 and dy != 0:
          raise ValueError(f"Both dx and dy have values: dx: {dx}, dy {dy}")
        if dx == 0:
          next_y_inclusive = next_y + sign(dy)
          for y in range(cur_y, next_y_inclusive, sign(dy)):
            self.grid.set(Point(x=cur_x, y=y), Objects.ROCK)
        if dy == 0:
          next_x_inclusive = next_x + sign(dx)
          for x in range(cur_x, next_x_inclusive, sign(dx)):
            self.grid.set(Point(x=x, y=cur_y), Objects.ROCK)
    
    self.sand_init = sand_init
    self.steps = 0
    self.floor_y = max_y + 2
    self.use_floor = use_floor

  def _check_point(self, pt: Point):
    grid_val = self.grid.get_oob(pt)
    if self.use_floor:
      if pt.y == self.floor_y:
        return MoveStatus.BLOCKED
      elif grid_val == None:
        min_x, max_x = self.grid.x_lims()
        update_pt = pt
        if pt.x <= min_x:
          update_pt = Point(pt.x - 10, pt.y)
        elif pt.x >= max_x:
          update_pt = Point(pt.x + 10, pt.y)
        self.grid.set(update_pt, Objects.AIR)
        return MoveStatus.MOVED
      elif grid_val == Objects.AIR:
        return MoveStatus.MOVED
      else:
        return MoveStatus.BLOCKED
    else:
      if grid_val == None:
        return MoveStatus.OOB
      elif grid_val == Objects.AIR:
        return MoveStatus.MOVED
      else:
        return MoveStatus.BLOCKED

  def step(self):
    self.steps += 1
    pt = self.sand_init
    trace = []
    status = MoveStatus.MOVED
    while status == MoveStatus.MOVED:
      pt_down = Point(pt.x, pt.y+1)
      down_status = self._check_point(pt_down)
      if down_status == MoveStatus.MOVED:
        pt = pt_down
      else:
        pt_down_left = Point(pt.x-1, pt.y+1)
        down_left_status = self._check_point(pt_down_left)
        if down_left_status == MoveStatus.MOVED:
          pt = pt_down_left
        else:
          pt_down_right = Point(pt.x+1, pt.y+1)
          down_right_status = self._check_point(pt_down_right)
          if down_right_status == MoveStatus.MOVED:
            pt = pt_down_right
          else:
            if down_status == MoveStatus.OOB or down_left_status == MoveStatus.OOB or down_right_status == MoveStatus.OOB:
              status = MoveStatus.OOB
            else:
              if self.use_floor and pt == self.sand_init:
                status = MoveStatus.AT_INIT
              else:
                status = MoveStatus.FIXED
          

      trace.append(pt)
    
    if status == MoveStatus.FIXED:
      self.grid.set(pt, Objects.SAND)
    elif status == MoveStatus.OOB:
      for p in trace:
        self.grid.set(p, Objects.TRACE)
    elif status == MoveStatus.AT_INIT:
      pass
    else:
      raise ValueError("How did you get here?")

    return status

  def print(self, fname=None):
    s = ""
    for row in self.grid.data:
      for elem in row:
        s += char_map[elem]
      s += "\n"
    if self.use_floor:
      if len(self.grid.data) != self.floor_y:
        for _ in self.grid.data[0]:
          s += char_map[Objects.AIR]
      for _ in self.grid.data[0]:
        s += char_map[Objects.ROCK]
      s += "\n"
    if fname:
      with open(fname, "w") as f:
        f.write(s)
    else:
      print(s)

def parse_input(rows):
  paths = []
  for row in rows:
    path = []
    points = row.split("->")
    for p in points:
      nums = p.strip().split(",")
      path.append(Point(x=int(nums[0]), y=int(nums[1])))
    paths.append(path)
  return paths

def part1():
  rock_paths = parse_input(data_rows)
  # print(rock_paths)
  sand_init = Point(x=500,y=0)
  sim = SandSim(rock_paths, sand_init)
  sim.print("start.txt")
  while True:
    status = sim.step()
    if status == MoveStatus.OOB:
      break
  sim.print("part1.txt")
  print(sim.steps-1)

# part1()

def part2():
  rock_paths = parse_input(data_rows)
  sand_init = Point(x=500,y=0)
  sim = SandSim(rock_paths, sand_init, use_floor=True)
  while True:
    status = sim.step()
    if status == MoveStatus.AT_INIT:
      break
  sim.print("part2.txt")
  print(sim.steps)

part2()