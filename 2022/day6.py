import sys
sys.path.append('.')
import aoc
import math

data_rows = aoc.get_input(6, sample=False, index=1).splitlines()

def part1():
  row = data_rows[0]
  for i in range(4, len(row)):
    s = set(row[i-4:i])
    if len(s) == 4:
      print(i)
      return

# part1()

def part2():
  row = data_rows[0]
  for i in range(14, len(row)):
    s = set(row[i-14:i])
    if len(s) == 14:
      print(i)
      return

part2()