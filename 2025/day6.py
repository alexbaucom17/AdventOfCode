
import sys
sys.path.append('.')
import aoc
from aoc_utils import parsing
import dataclasses
import math

@dataclasses.dataclass(frozen=True)
class Problem:
  nums: list[int]
  op: str

  def solve(self):
    if self.op == '+':
      return sum(self.nums)
    elif self.op == "*":
      return math.prod(self.nums)
    else:
      raise ValueError("No operator")

data_rows = aoc.get_input(day=6, sample=False, index=0).splitlines()

def parse1(data_rows: list[str]) -> list[Problem]:
  grid = [row.split() for row in data_rows]
  num_strs = grid[:-1]
  ops = grid[-1]

  problems = []
  for col in range(len(ops)):
    op = ops[col]
    nums = []
    for row in range(len(num_strs)):
      nums.append(int(num_strs[row][col]))
    problems.append(Problem(nums, op))
  return problems

def part1():
  problems = parse1(data_rows)
  total = 0
  for p in problems:
    # print(p)
    # print(p.solve())
    total += p.solve()
  print(total)

# part1()

def find_column_breaks(data_rows: list[str]) -> set[int]:
  col_gaps = set()
  for j,row in enumerate(data_rows):
    s = set()
    for i,c in enumerate(row):
      if c == ' ':
        s.add(i)
    if j == 0:
      col_gaps = s
    else:
      col_gaps &= s
  return col_gaps


def parse2(data_rows: list[str]) -> list[Problem]:
  col_gaps = sorted(list(find_column_breaks(data_rows)))
  cols = [[] for i in range(len(col_gaps) + 1)]
  for row in data_rows[:-1]:
    for i in range(len(col_gaps)+1):
      if i == 0:
        val = row[0:col_gaps[0]]
      elif i == len(col_gaps):
        val = row[col_gaps[i-1]+1:]
      else:
        val = row[col_gaps[i-1]+1:col_gaps[i]]
      cols[i].append(val) 
  ops = data_rows[-1].split()  

  nums = []
  for c in cols:
    new_nums = [char for char in c[0]]
    for row in c[1:]:
      for i,char in enumerate(row):
        new_nums[i] += char
    nums.append(new_nums)

  problems = []
  for num,op in zip(nums, ops):
    int_nums = [int(n) for n in num]
    problems.append(Problem(int_nums, op))
  
  return problems

def part2():
  problems = parse2(data_rows)
  total = 0
  for p in problems:
    # print(p)
    # print(p.solve())
    total += p.solve()
  print(total)

part2()

