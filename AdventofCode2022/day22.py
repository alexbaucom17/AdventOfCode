import sys
sys.path.append('.')
import aoc
import math
import numpy as np
import enum
from aoc_utils.parsing import group_by_blank_lines
from dataclasses import dataclass

use_sample = False
data_rows = aoc.get_input(22, sample=use_sample, index=0).splitlines()

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

# part1()

class CubeFaceGrid:
  def __init__(self, data):
    self.data = data
    self.x_max = self.data.shape[1]
    self.y_max = self.data.shape[0]

  def get_xy(self, xy):
    x = xy[0]
    y = self.y_max - xy[1] - 1
    if not self._in_bounds(xy):
      return INVALID
    try:
      val = self.data[y, x]
    except IndexError:
      return INVALID
    return val

  def _in_bounds(self, xy):
    if np.any(xy < np.asarray([0,0], dtype=int)) or np.any(xy >= np.asarray([self.x_max, self.y_max], dtype=int)):
      return False
    return True

  def step(self, xy, dir):
    new_xy = xy + dir
    wrap = False
    new_val = new_xy
    stopped = False
    val = self.get_xy(new_xy)
    if val == INVALID:
      wrap = True
      new_val = xy
    elif val == BLOCKED:
      new_val = xy
      stopped = True

    return (new_val, stopped, wrap)

@dataclass
class WrapInfo:
  point: np.array
  dir: np.array
  face: int

def extract_cube_faces(rows, face_size):
  # Generate full 2d grid and validate dimensions
  full_grid = NonSquareGridWithWrapping(rows)
  if full_grid.x_max % face_size != 0 or full_grid.y_max % face_size != 0:
    raise ValueError(f"Full grid has size [{full_grid.x_max}, {full_grid.y_max}] which is not divisible by face size {face_size}")
  x_steps = int(full_grid.x_max / face_size)
  y_steps = int(full_grid.y_max / face_size)

  # Split full grid into faces
  data_coords = []
  for ix in range(x_steps):
    for iy in range(y_steps):
      row_col_corner = np.asarray([ix*face_size, iy * face_size ], dtype=int)
      row_col_lower_corner = row_col_corner + np.asarray([face_size, face_size], dtype=int)
      data = full_grid.data[row_col_corner[1]:row_col_lower_corner[1], row_col_corner[0]:row_col_lower_corner[0]]
      block_coords = (ix, iy)
      xy_corner_coord = np.asarray([row_col_corner[0], full_grid.y_max - (row_col_corner[1] + face_size)])
      data_coords.append((xy_corner_coord, block_coords, data))
  print(f"Split full grid into {len(data_coords)} boxes")

  # Determine valid faces
  valid_faces = []
  id = 1
  for coord, block_coord, data in data_coords:
    if np.all(data == INVALID): continue
    else:
      valid_faces.append((coord, block_coord, data, id))
      id += 1
  if len(valid_faces) != 6:
    raise ValueError(f"Expected 6 faces from input data, got {len(valid_faces)} instead")
  print("Detected 6 faces in input data")

  # dict[face_id, CubeFaceGrid]
  face_data = {id: CubeFaceGrid(data) for _, _, data, id in valid_faces}
  # dict[face_id, point]
  unwrap_coords = {id: coord for coord, _, _, id in valid_faces}
  # dict[face_id, dict[point, wrap_info]]
  edge_mappings = {id: {d: {} for d in [(-1,0), (1,0), (0,1), (0,-1)]} for _, _, _, id in valid_faces}

  # Display block view to help edge mapping
  blocks = [[None for ix in range(x_steps)] for iy in range(y_steps)]
  for _, block_coord, _, id in valid_faces:
    blocks[block_coord[1]][block_coord[0]] = id
  s = ""
  for row in blocks:
    for upper in [True, False]:
      for val in row:
        if val is None:
          s += " " * 7
        else:
          if upper:
            s += f" {val}a {val}b "
          else:
            s += f" {val}d {val}c "
      s += "\n"
  print(s)

  edge_pairs_sample = [
    (("4a", "4d"), ("2b", "2c")),
    (("4a", "4b"), ("3d", "3c")),
    (("4b", "4c"), ("6b", "6a")),
    (("4c", "4d"), ("5b", "5a")),
    (("2a", "2b"), ("3a", "3d")),
    (("3b", "3c"), ("6c", "6b")),
    (("6d", "6a"), ("5c", "5b")),
    (("5d", "5a"), ("2d", "2c")),
    (("1a", "1b"), ("3a", "3b")),
    (("1b", "1c"), ("2a", "2d")),
    (("1c", "1d"), ("5d", "5c")),
    (("1d", "1a"), ("6d", "6c")),
  ]
  edge_pairs_full = [
    (("4a", "4d"), ("1a", "1b")),
    (("4a", "4b"), ("3d", "3c")),
    (("4b", "4c"), ("6d", "6c")),
    (("4c", "4d"), ("5b", "5a")),
    (("3a", "3d"), ("1d", "1a")),
    (("3b", "3c"), ("6a", "6d")),
    (("5a", "5d"), ("1b", "1c")),
    (("5b", "5c"), ("6c", "6b")),
    (("2a", "2b"), ("1d", "1c")),
    (("2b", "2c"), ("5d", "5c")),
    (("2c", "2d"), ("6b", "6a")),
    (("2d", "2a"), ("3b", "3a")),
  ]

  if use_sample:
    edge_pairs = edge_pairs_sample
  else:
    edge_pairs = edge_pairs_full

  letter_to_point = {
    "a": np.asarray((0,face_size-1), dtype=int),
    "b": np.asarray((face_size-1, face_size-1), dtype=int),
    "c": np.asarray((face_size-1, 0), dtype=int),
    "d": np.asarray((0, 0), dtype=int)
  }
  edge_to_dir = {
    "ab": np.asarray([0, -1], dtype=int),
    "bc": np.asarray([-1, 0], dtype=int),
    "cd": np.asarray([0, 1], dtype=int),
    "ad": np.asarray([1, 0], dtype=int),
  }

  for p1, p2 in edge_pairs:
    face1 = int(p1[0][0])
    face1_start_point = letter_to_point[p1[0][1]]
    face1_end_point = letter_to_point[p1[1][1]]
    face1_dp = face1_end_point - face1_start_point
    face1_step = face1_dp / np.linalg.norm(face1_dp)
    face1_edge = "".join(sorted([p1[0][1], p1[1][1]]))
    face1_perp = edge_to_dir[face1_edge]

    face2 = int(p2[0][0])
    face2_start_point = letter_to_point[p2[0][1]]
    face2_end_point = letter_to_point[p2[1][1]]
    face2_dp = face2_end_point - face2_start_point
    face2_step = face2_dp / np.linalg.norm(face2_dp)
    face2_edge = "".join(sorted([p2[0][1], p2[1][1]]))
    face2_perp = edge_to_dir[face2_edge]

    for step_ix in range(face_size):
      f1_point = (face1_start_point + face1_step * step_ix).astype(int)
      f2_point = (face2_start_point + face2_step * step_ix).astype(int)
      edge_mappings[face1][tuple(-face1_perp)][tuple(f1_point)] = WrapInfo(f2_point, face2_perp, face2)
      edge_mappings[face2][tuple(-face2_perp)][tuple(f2_point)] = WrapInfo(f1_point, face1_perp, face1)

  return (face_data, edge_mappings, unwrap_coords)

class CubeGrid:

  def __init__(self, data_rows, face_size=4):
    cube_face_data = extract_cube_faces(data_rows, face_size)
    self.raw_data = data_rows
    self.data = cube_face_data[0]
    self.edge_mappings = cube_face_data[1]
    self.unwrap_coords = cube_face_data[2]
    
  def do_step(self, xy, face, dir, step):
    if step == "L" or step == "R":
      dir = rotate(dir, step)
    else:
      for i in range(step):
        xy, dir, face, stopped = self._wrapped_step(xy, face, dir)
        # print(f"do_step: at {xy} on face {face}, facing {dir}")
        if stopped:
          break
    return xy, face, dir

  def _wrapped_step(self, xy, face, dir):
    new_xy, stopped, wrap = self.data[face].step(xy, dir)
    if wrap:
      try:
        wrap_info = self.edge_mappings[face][tuple(dir)][tuple(xy)]
      except KeyError:
        print(f"Could not find keys for {face}, {tuple(dir)}, {tuple(xy)} in edge mappings")
        print(self.edge_mappings[face].keys())
        print([len(x) for x in self.edge_mappings[face].values()])
      wrap_xy = wrap_info.point
      wrap_dir = wrap_info.dir
      wrap_face = wrap_info.face
      new_val = self.data[wrap_face].get_xy(wrap_xy)
      if new_val == BLOCKED:
        stopped = True
        new_face = face
        new_dir = dir
      elif new_val == INVALID:
        raise ValueError(f"Got invalid result for _wrapped_step({xy},{face},{dir}) where wrap_info is {wrap_info}")
      else:
        new_xy = wrap_xy
        new_dir = wrap_dir
        new_face = wrap_face
    else:
      new_face = face
      new_dir = dir
  
    return new_xy, new_dir, new_face, stopped

  def to_pass_unwrapped(self, xy, face, dir):
    unwrapped_xy = self.unwrap_coords[face] + xy
    print(f"unwrap coords: {self.unwrap_coords[face]}")
    print(f"unwrapped_xy: {unwrapped_xy}")
    y_max = len(self.raw_data)
    print(y_max)
    return to_pass(unwrapped_xy, dir, y_max)


def part2():
  grid_rows, step_rows = group_by_blank_lines(data_rows)
  face_size = 4 if use_sample else 50
  grid = CubeGrid(grid_rows, face_size)
  steps = parse_steps(step_rows)

  if use_sample:
    face = 3
  else:
    face = 3
  start_y = grid.data[face].y_max - 1
  start_x = 0

  xy = np.asarray([start_x, start_y], dtype=int)
  dir = np.asarray([1,0], dtype=int)
  # print(f"at {xy} on face {face}, facing {dir}")
  for step in steps:
    xy, face, dir = grid.do_step(xy, face, dir, step)
    # print(f"at {xy} on face {face}, facing {dir}")
  print(f"at {xy} on face {face}, facing {dir}")
  print(grid.to_pass_unwrapped(xy, face, dir))

part2()