
import sys
sys.path.append('.')
import aoc
from aoc_utils import parsing
import queue

data_rows = aoc.get_input(day=7, sample=False, index=0).splitlines()


def part1():
  data_dict = {}
  start_loc = (0,0)
  for i, row in enumerate(data_rows):
    for j, c in enumerate(row):
      loc = (i,j)
      data_dict[loc] = c
      if c == 'S':
        start_loc = loc

  # bfs
  q = queue.Queue()
  start_loc = (start_loc[0]+1, start_loc[1])
  q.put(start_loc)
  total_splits = 0
  explored = set()

  while not q.empty():
    loc = q.get()
    if loc in explored:
      continue

    explored.add(loc)
    next_loc = (loc[0]+1, loc[1])

    if next_loc not in data_dict:
      continue

    if data_dict[next_loc] == '.':
      q.put(next_loc)
      continue

    if data_dict[next_loc] == '^':
      total_splits += 1
      l1 = (next_loc[0], next_loc[1]+1)
      if l1 not in explored:
        q.put(l1)
      l2 = (next_loc[0], next_loc[1]-1)
      if l2 not in explored:
        q.put(l2)

  print(total_splits)  
  
# part1()

def part2():
  data_dict = {}
  for i, row in enumerate(reversed(data_rows)):
    splits = []
    for j, c in enumerate(row):
      loc = (i,j)
      if c == '^':
        splits.append(loc)
      elif c == '.':
        if i == 0:
          data_dict[loc] = 1
        else:
          gather_loc = (loc[0]-1, loc[1])
          data_dict[loc] = data_dict[gather_loc]
      elif c == 'S':
        gather_loc = (loc[0]-1, loc[1])
        print(data_dict[gather_loc])
        break
      else:
        raise ValueError(f"Unknown char {c}")
    for split in splits:
      gather_left = (split[0], split[1]-1)
      gather_right = (split[0], split[1]+1)
      data_dict[split] = data_dict[gather_left] + data_dict[gather_right]

part2()

