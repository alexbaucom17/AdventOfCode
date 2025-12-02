
import sys
sys.path.append('.')
import aoc
from aoc_utils import parsing
import functools

data_rows = aoc.get_input(day=2, sample=False, index=0).splitlines()

def is_invalid_1(num: int) -> bool:
    i_str = str(num)
    strlen = len(i_str)
    if strlen % 2 == 1:
      return False
    half = int(strlen/2)
    front = i_str[:half]
    back = i_str[half:]
    return front == back

@functools.cache
def get_divisors(n: int) -> list[int]:
  divisors = []
  for i in range(2, n+1):
    if n % i == 0:
      divisors.append(i)
  return divisors

def split_even(s: str, d: int) -> list[str]:
  if len(s) % d != 0:
    raise ValueError("String length not divisible by divisor")

  splits = []
  split_size = len(s) // d
  for i in range(d):
    splits.append(s[i*split_size:(i+1)*split_size])
  return splits

def is_invalid_2(num: int) -> bool:
    i_str = str(num)
    strlen = len(i_str)
    divs = get_divisors(strlen)
    # print(f"Checking num: {num}")
    # print(f"Divisors: {divs}")
    for d in divs:
      splits = split_even(i_str, d)
      # print(f'Checking split length {d}: {splits}')
      if all(s == splits[0] for s in splits):
        return True
      
    return False

def part1():
  ranges = data_rows[0].split(',')
  total = 0

  for r in ranges:
    start, end = r.split('-')
    print(f"Checking range [{start}, {end}]")

    for i in range(int(start), int(end)+1):
      if is_invalid_1(i):
        print(f"Found repeat: {i}")
        total += i
  print(total)


# part1()

def part2():
  ranges = data_rows[0].split(',')
  total = 0

  for r in ranges:
    start, end = r.split('-')
    print(f"Checking range [{start}, {end}]")

    for i in range(int(start), int(end)+1):
      if is_invalid_2(i):
        print(f"Found repeat: {i}")
        total += i
  print(total)

part2()

