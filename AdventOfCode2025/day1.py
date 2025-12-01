import sys
sys.path.append('.')
import aoc
import math

data_rows = aoc.get_input(1, sample=False, index=0).splitlines()

def part1():
  current = 50
  num_zeros = 0

  for row in data_rows:
    dir = row[0]
    val = int(row[1:])
    if dir == 'L':
      current -= val
    else:
      current += val

    current = current % 100

    if current == 0:
      num_zeros += 1
    
    # print(f"{row} -> {current}")
  print(num_zeros)

# part1()

def part2():
  current = 50
  num_zeros = 0

  for row in data_rows:
    dir = row[0]
    val = int(row[1:])

    q, r = divmod(val, 100)
    # print(f"{q},{r}")
    num_zeros += q

    if dir == 'L':
      if current == 0:
        num_zeros -= 1
      current -= r
    else:
      current += r

    if current == 0:
      num_zeros += 1
    
    if current >= 100 or current < 0:
      num_zeros += 1
      current = current % 100
    
    # print(f"{row} -> {current}, 0: {num_zeros}")
  print(num_zeros)

part2()