
import sys
sys.path.append('.')
import aoc
from aoc_utils import parsing, misc

data_rows = aoc.get_input(day=5, sample=False, index=0).splitlines()
groups = parsing.group_by_blank_lines(data_rows)

def parse_fresh(rows: list[str]) -> list[list[int]]:
  db = []
  for row in rows:
    start,end = row.split('-')
    db.append([int(start), int(end)])
  return db

fresh_rows = parse_fresh(groups[0])
ids = [int(row) for row in groups[1]]

def is_fresh(id):
  for fresh_range in fresh_rows:
    if (id >= fresh_range[0] and id <= fresh_range[1]):
      return True
  return False

def part1():
  total = 0
  for id in ids:
    if is_fresh(id):
      total += 1
  print(total)

# part1()

def part2():
  total = 0
  fresh_rows_set = set(tuple(r) for r in fresh_rows)
  merged_ranges = misc.merge_1d_ranges_simple(fresh_rows_set)
  for r in merged_ranges:
    print(r)
    diff = r[1] - r[0] + 1
    print(diff)
    total += diff
  print(total)


part2()

