import sys
sys.path.append('.')
import aoc
import math
from aoc_utils.parsing import group_by_blank_lines
import enum
from functools import cmp_to_key

data_rows = aoc.get_input(13, sample=False, index=0).splitlines()

class CheckState(enum.Enum):
  UNKNOWN = 0
  INVALID = 1
  VALID = 2

def check_order(left, right):
  if type(left) == int and type(right) == int:
    if left < right:
      return CheckState.VALID
    elif right < left:
      return CheckState.INVALID
    else:
      return CheckState.UNKNOWN
  
  if type(left) == list and type(right) == list:
    min_length = min(len(left), len(right))
    for i in range(min_length):
      status = check_order(left[i], right[i])
      if status != CheckState.UNKNOWN:
        return status
    if len(left) < len(right):
      return CheckState.VALID
    elif len(right) < len(left):
      return CheckState.INVALID
    else:
      return CheckState.UNKNOWN

  if type(left) == int and type(right) == list:
    return check_order([left], right)
  if type(left) == list and type(right) == int:
    return check_order(left, [right])

  raise ValueError(f"Could not match rule for left={left}, type={type(left)} | right={right}, type={type(right)}")

    

def part1():
  pairs = group_by_blank_lines(data_rows)
  total = 0
  for i, pair in enumerate(pairs):
    left = eval(pair[0])
    right = eval(pair[1])
    status = check_order(left, right)
    print(left)
    print(right)
    print(status)
    if status == CheckState.VALID:
      total += i + 1

  print(total)

# part1()

def part2():
  data = []
  for row in data_rows:
    if row.strip():
        data.append(eval(row))
  data.append([[2]])
  data.append([[6]])

  status_map = {CheckState.INVALID: 1, CheckState.UNKNOWN: 0, CheckState.VALID: -1}
  def cmp(left, right):
    status = check_order(left, right)
    return status_map[status]

  data.sort(key=cmp_to_key(cmp))
  # for elem in data:
  #   print(elem)
  decoder_key = 1
  for i, elem in enumerate(data):
    if elem == [[2]] or elem == [[6]]:
      print(f"Found {elem} at index {i+1}")
      decoder_key *= (i+1)
  print(decoder_key)

part2()