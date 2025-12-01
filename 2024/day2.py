
import sys
sys.path.append('.')
import aoc
from aoc_utils import parsing

data_rows = aoc.get_input(day=2, sample=False, index=0).splitlines()

def get_diffs_1(levels: list[int]) -> list[int]:
  return [levels[i] - levels[i+1] for i in range(len(levels) - 1)]

def get_diffs_2(levels: list[int]) -> list[list[int]]:
  diffs = [get_diffs_1(levels)]
  for skip in range(len(levels)):
    new_levels = [levels[i] for i in range(len(levels)) if i != skip]
    diffs.append(get_diffs_1(new_levels))
  return diffs

def is_safe(diffs: list[int]) -> bool:
  if all(x > 0 for x in diffs) or all(x < 0 for x in diffs):
    if all(abs(x) >= 1 and abs(x) <= 3 for x in diffs):
      return True

  return False

def part1():
  num_safe = 0
  for row in data_rows:
    levels = parsing.get_numbers_with_separator(row)
    diffs = get_diffs_1(levels)
    # print(levels)
    if is_safe(diffs):
      num_safe += 1
  print(num_safe)

# part1()

def part2():
  num_safe = 0
  for row in data_rows:
    levels = parsing.get_numbers_with_separator(row)
    all_diffs = get_diffs_2(levels)
    # print(levels)
    for diff in all_diffs:
      # print(diff)
      if is_safe(diff):
        num_safe += 1
        # print("safe")
        break
      
    # print("-------")

  print(num_safe)

part2()

