
import sys
sys.path.append('.')
import aoc
from aoc_utils import parsing
from collections import Counter

data_rows = aoc.get_input(day=1, sample=False, index=0).splitlines()

def part1():
  c1 = []
  c2 = []
  for row in data_rows:
    n1, n2 = parsing.get_numbers_with_separator(row)
    c1.append(n1)
    c2.append(n2)
  
  total = 0
  for a, b in zip(sorted(c1), sorted(c2)):
    diff = abs(a-b)
    total += diff
    
    # print(f"a: {a}, b: {b}, diff: {diff}")

  print(total)
  

# part1()

def part2():
  l1 = []
  l2 = []
  for row in data_rows:
    n1, n2 = parsing.get_numbers_with_separator(row)
    l1.append(n1)
    l2.append(n2)
  c2 = Counter(l2)
  
  total = 0
  for n in l1:
    num_instances = c2[n]
    similarity = n * num_instances
    total += similarity
    
    # print(f"n: {n}, num_instances: {num_instances}, similarity: {similarity}")

  print(total)

part2()

