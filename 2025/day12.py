
import sys
sys.path.append('.')
import aoc
from aoc_utils import parsing
import dataclasses
import numpy as np
from collections import defaultdict

data_rows = aoc.get_input(day=12, sample=False, index=0).splitlines()
groups = parsing.group_by_blank_lines(data_rows)
shape_groups = groups[:-1]
region_group = groups[-1]

@dataclasses.dataclass
class Shape:
  id: int
  size: int
  area: int
  shape: np.ndarray

@dataclasses.dataclass
class Region:
  id: int
  width: int
  length: int
  num_shapes: list[int]

def parse_shapes(shape_groups) -> list[Shape]:
  shapes = []
  for shape_strs in shape_groups:
    id = int(shape_strs[0][0])
    # Assumes equal size for length and width since my puzzle input has that
    size = len(shape_strs[1])
    shape = np.array([[ c=='#' for c in row] for row in shape_strs[1:]], dtype=bool)
    shapes.append(Shape(id, size, np.sum(np.sum(shape)), shape))

  return shapes

def parse_regions(region_group) -> list[Region]:
  regions = []
  id = 0
  for region_str in region_group:
    strs = region_str.split(' ')
    wxl = strs[0].split('x')
    width = int(wxl[0])
    length = int(wxl[1][:-1])
    num_shapes = map(int, strs[1:])
    regions.append(Region(id, width, length, list(num_shapes)))
    id += 1

  return regions

def definitely_too_big(region: Region, shapes: list[Shape]) -> bool:
  region_area = region.length * region.width
  shape_area = 0
  for i, shape in enumerate(shapes):
    num_shapes = region.num_shapes[i]
    shape_area += num_shapes * shape.area
  
  return shape_area > region_area


def shapes_fit(region: Region, shapes: list[Shape]) -> 'str':
  if definitely_too_big(region, shapes):
    return 'def_too_big'
  # if definitely_fits_no_overlap(region, shapes):
  #   return 'def_fits'
  return 'unknown'


def part1():
  shapes = parse_shapes(shape_groups)
  regions = parse_regions(region_group)
  totals = defaultdict(int)
  for region in regions:
    result = shapes_fit(region, shapes)
    totals[result] += 1
    print(f"{region.id}: {result}")

  print(totals)


part1()

#def part2():
#  pass

#part2()

