import sys
sys.path.append('.')
import aoc
import math
from aoc_utils import parsing
import numpy as np

data_rows = aoc.get_input(9, sample=False, index=0).splitlines()

def process_row(row, reverse=False):
  rows = [row]
  while not np.all(rows[-1] == 0):
    rows.append(np.diff(rows[-1]))

  if reverse:
    start_vals = [r[0] for r in rows]
    running_val = 0
    for i in range(len(start_vals), 0, -1):
      running_val = start_vals[i-1] - running_val
    return running_val
  else:
    end_vals = [r[-1] for r in rows]
    running_val = 0
    for i in range(len(end_vals), 0, -1):
      running_val += end_vals[i-1]
    return running_val

def part1():
  seqs = [np.asarray(parsing.get_numbers_with_separator(row)) for row in data_rows]
  print(sum([process_row(s) for s in seqs]))

# part1()

def part2():
  seqs = [np.asarray(parsing.get_numbers_with_separator(row)) for row in data_rows]
  print(sum([process_row(s, reverse=True) for s in seqs]))

part2()