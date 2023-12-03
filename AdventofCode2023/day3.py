import sys
sys.path.append('.')
import aoc
import math
import copy
from aoc_utils import grid
import numpy as np
import collections

data_rows = aoc.get_input(3, sample=False, index=0).splitlines()

numpy_diags = [np.asarray(t) for t in grid.ortho_diag_neighbors()]

def parse_row(row: str, row_num: int, number_mapping: list, symbol_set: set, gear_set: set):
  mid_num = False
  active_num = ""
  active_num_adj = set()

  def add_to_set(m_set, coord, offsets):
    for offset in offsets:
        m_set.add(tuple(coord + offset))

  for col_num, c in enumerate(row):
    rowcol = np.asarray([row_num, col_num])
    if c in "0123456789":
      if mid_num:
        active_num += c
        add_to_set(active_num_adj, rowcol, numpy_diags)
      else:
        mid_num = True
        active_num += c
        add_to_set(active_num_adj, rowcol, numpy_diags)

    else:
      if mid_num:
        mid_num = False
        number_mapping.append((int(active_num), copy.deepcopy(active_num_adj)))
        active_num = ""
        active_num_adj = set()

      if c in ".":
        continue
      else:
        # This is a symbol
        symbol_set.add(tuple(rowcol))
        if c == "*":
          gear_set.add(tuple(rowcol))

  
  if mid_num:
    number_mapping.append((int(active_num), copy.deepcopy(active_num_adj)))


def build_maps():
  number_map = []
  symbol_set = set()
  gear_set = set()
  for row_num, row in enumerate(data_rows):
    parse_row(row, row_num, number_map, symbol_set, gear_set)

  return (number_map, symbol_set, gear_set)

def part1():
  number_map, symbol_set,_ = build_maps()
  total = 0
  for num, coord_set in number_map:
    intersection = coord_set & symbol_set
    if intersection:
      total += num
  print(total)

# part1()

def build_gear_map(number_map: list, gear_set: set)-> dict:
  gear_map = collections.defaultdict(list)
  for num, coord_set in number_map:
    intersection = coord_set & gear_set
    if intersection:
      if len(intersection) > 1:
        raise ValueError(f"more than one intersection found for {num}, {intersection}")
      
      gear_map[intersection.pop()].append(num)
  return gear_map
    

def part2():
  number_map, _, gear_set = build_maps()
  gear_map = build_gear_map(number_map, gear_set)
  total = 0
  for values in gear_map.values():
    if len(values) == 2:
      total += values[0] * values[1]
  print(total)

part2()