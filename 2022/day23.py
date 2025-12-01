import sys
sys.path.append('.')
import aoc
import math
import numpy as np
from aoc_utils.grid import ortho_diag_neighbors
from collections import defaultdict

data_rows = aoc.get_input(23, sample=False, index=0).splitlines()

def get_locations_from_input(data_rows):
  locations = []
  for i, row in enumerate(reversed(data_rows)):
    for j, char in enumerate(row):
      if char == "#":
        locations.append((j,i))
  return locations

def north_adders():
  return [(-1,1), (0,1), (1,1)]

def east_adders():
  return [(1,1), (1,0), (1,-1)]

def south_adders():
  return [(1,-1), (0,-1), (-1,-1)]

def west_adders():
  return [(-1,-1), (-1,0), (-1,1)]

def apply_adder(location, adder_fn):
  vals = []
  for adder in adder_fn():
    vals.append((location[0] + adder[0], location[1] + adder[1]))
  return vals

def build_dir_map():
  all_steps = ortho_diag_neighbors()
  dir_map = {}
  for char, adder in [("N", north_adders), ("E", east_adders), ("S", south_adders), ("W", west_adders)]:
    adder_steps = adder()
    all_step_idx = []
    for step in adder_steps:
      all_step_idx.append(all_steps.index(step))
    dir_map[char] = all_step_idx
  return dir_map

def generate_proposals(locations, dir_map, dir_ordering):
  new_locations_moving_with_source = []
  new_locations_not_moving = []
  for location in locations:

    all_adjacent = apply_adder(location, ortho_diag_neighbors)
    adjacent_occupied = [(coord in locations) for coord in all_adjacent]
    any_adjacent_occupied = np.any(adjacent_occupied)

    if not any_adjacent_occupied:
      new_locations_not_moving.append(location)
      continue

    new_location = None
    for dir in dir_ordering:
      dir_idx = dir_map[dir]
      location_filled = [adjacent_occupied[i] for i in range(len(adjacent_occupied)) if i in dir_idx]
      if not location_filled[0] and not location_filled[1] and not location_filled[2]:
        new_location = all_adjacent[dir_idx[1]]
        break
    if new_location is None:
      new_locations_not_moving.append(location)
    else:
      new_locations_moving_with_source.append((new_location, location))

  return new_locations_moving_with_source, new_locations_not_moving

def filter_duplicate_proposals(proposals):
  freq = defaultdict(list)
  for i,new_loc in enumerate(proposals):
    freq[new_loc[0]].append(i)
  unique_locations_moving_with_source = {}
  duplicate_locations_not_moving = []
  # print(freq)
  for loc, items in freq.items():
    if len(items) > 1:
      for i in items:
        duplicate_locations_not_moving.append(proposals[i][1])
    else:
      unique_locations_moving_with_source[loc] = proposals[items[0]][1]

  return unique_locations_moving_with_source, duplicate_locations_not_moving

def step(locations, dir_map, dir_ordering):

  proposed_locations_moving, locations_not_moving = generate_proposals(locations, dir_map, dir_ordering)
  # print("Locations moving")
  # for new_loc, old_loc in proposed_locations_moving:
  #   print(f"{new_loc}, {old_loc}")
  # print("Locations fixed")
  # for l in locations_not_moving:
  #   print(l)

  unique_locations_moving_with_source, duplicate_locations_not_moving = filter_duplicate_proposals(proposed_locations_moving)
  # print("unique_locations_moving_with_source")
  # for new_loc, old_loc in unique_locations_moving_with_source.items():
  #   print(f"{new_loc}, {old_loc}")
  # print("duplicate_locations_not_moving")
  # for l in duplicate_locations_not_moving:
  #   print(l)

  new_locations = set(list(unique_locations_moving_with_source.keys()) + duplicate_locations_not_moving + locations_not_moving)
  no_moves = len(unique_locations_moving_with_source) == 0
  new_dir_ordering = dir_ordering[1:] + [dir_ordering[0]]
  return new_locations, new_dir_ordering, no_moves

def get_min_bounding(locations):
  min_x = 1000
  min_y = 1000
  max_x = -1000
  max_y = -10000
  for loc in locations:
    min_x = min(loc[0], min_x)
    min_y = min(loc[1], min_y)
    max_x = max(loc[0], max_x)
    max_y = max(loc[1], max_y)
  
  return (min_x, min_y), (max_x+1, max_y+1)

def draw(locations):
  min_bounds, max_bounds = get_min_bounding(locations)
  min_bounds = np.asarray(min_bounds, dtype=int)
  # print(min_bounds)
  max_bounds = np.asarray(max_bounds, dtype=int)
  # print(max_bounds)
  range_bounds = max_bounds - min_bounds
  # print(range_bounds)
  data = np.zeros(range_bounds, dtype=int).transpose()
  # print(data)
  for loc in locations:
    # print(loc)
    new_loc = np.asarray(loc,dtype=int) - min_bounds
    data[new_loc[1], new_loc[0]] = 1
  print(np.flipud(data))
   
def part1():
  locations = set(get_locations_from_input(data_rows))
  dir_map = build_dir_map()
  dir_ordering = ["N", "S", "W", "E"]

  for i in range(10):
    locations, dir_ordering, _ = step(locations, dir_map, dir_ordering)
    # print("-------")
    # print(locations)
    # print(dir_ordering)
    # draw(locations)

  min_bounds, max_bounds = get_min_bounding(locations)
  # print(min_bounds)
  # print(max_bounds)
  area = (max_bounds[0] - min_bounds[0]) * (max_bounds[1] - min_bounds[1])
  empty_spaces = area - len(locations)
  print(empty_spaces)

# part1()

def part2():
  locations = set(get_locations_from_input(data_rows))
  dir_map = build_dir_map()
  dir_ordering = ["N", "S", "W", "E"]
  count = 0

  while True:
    count += 1
    locations, dir_ordering, no_moves = step(locations, dir_map, dir_ordering)
    if no_moves:
      break

    if count % 100 == 0:
      print(f"On round {count}")

  print(count)

part2()