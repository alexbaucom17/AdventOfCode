import sys
sys.path.append('.')
import aoc
import math
from aoc_utils import grid
import numpy as np

data_rows = aoc.get_input(11, sample=False, index=0).splitlines()

def solve(offset: int):
  g = grid.grid_from_str(data_rows).numpy()
  empty_rows = np.where(np.all(g == 0, axis=1))
  empty_cols = np.where(np.all(g == 0, axis=0))
  xs, ys = np.where(g == 1)
  ids = np.arange(len(xs)) + 1

  def expanded_diff(c1, c2, empty_ix) -> int:
    if c1 < c2:
      count = np.sum(np.logical_and(empty_ix > c1, empty_ix < c2))
    else:
      count = np.sum(np.logical_and(empty_ix > c2, empty_ix < c1))
    return max(abs(c1 - c2) + count * (offset-1), 0)

  total_dist = 0
  for i in range(len(ids) - 1):
    for j in range(i+1, len(ids)):
      dx = expanded_diff(xs[i], xs[j], empty_rows)
      dy = expanded_diff(ys[i], ys[j], empty_cols)
      dist = dx + dy
      # print(f"Checked pair {ids[i]} ({xs[i]}, {ys[i]}), {ids[j]} ({xs[j]}, {ys[j]}), dist: {dist} ({dx}, {dy})")
      total_dist += dist
  print(f"Total dist: {total_dist}")


def part1():
  solve(offset=2)

# part1()

def part2():
  solve(offset=1000000)

part2()