
import sys
sys.path.append('.')
import aoc
from aoc_utils import parsing
import numpy as np

data_rows = aoc.get_input(day=3, sample=False, index=0).splitlines()

def max_joltage(bank: list[int]) -> int:
  max_index = np.argmax(bank[:-1])
  max_val = bank[max_index]
  next_max_val = max(bank[max_index+1:])
  return max_val * 10 + next_max_val

def max_joltage_recursive(bank: list[int], start_index: int, n_remaining: int) -> int:
  if n_remaining == 1:
    return max(bank[start_index:])
  
  max_index = start_index + int(np.argmax(bank[start_index:-(n_remaining-1)]))
  max_val = bank[max_index]
  return max_val * pow(10, n_remaining-1) + max_joltage_recursive(bank, max_index+1, n_remaining-1)


def part1():
  int_data = parsing.int_grid(data_rows)
  
  total = 0
  for bank in int_data:
    j = max_joltage(bank)
    # print(f"bank: {bank} -> {j}")
    total += j

  print(total)

# part1()

def part2():
  int_data = parsing.int_grid(data_rows)
  
  total = 0
  for bank in int_data:
    j = max_joltage_recursive(bank, 0, 12)
    # print(f"bank: {bank} -> {j}")
    total += j

  print(total)

part2()

