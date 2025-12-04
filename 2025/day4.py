
import sys
sys.path.append('.')
import aoc
from aoc_utils import parsing
from aoc_utils import grid
import queue

data_rows = aoc.get_input(day=4, sample=False, index=0).splitlines()
g = grid.grid_from_str(data_rows, '.', "@")

def is_accessible(g, c):
  neighbors = g.get_neighbors(c, grid.ortho_diag_neighbors)
  full_neighbors = 0
  for _, val in neighbors:
    if val == 1:
      full_neighbors += 1
  if full_neighbors < 4:
    return True
  return False

def get_accessible_rolls(g):
  rolls = []
  for col_ix in range(g.n_cols):
    for row_ix in range(g.n_rows):
      c = grid.Coord(row_ix, col_ix)
      if g.safe_get(c) != 1:
        continue
      if is_accessible(g, c):
        rolls.append(c)
  return rolls

def part1():
  rolls = get_accessible_rolls(g)
  print(len(rolls))

# part1()

def part2():
  starting_rolls = get_accessible_rolls(g)
  q = queue.Queue()
  for r in starting_rolls:
    q.put(r)

  total_removed = 0
  while not q.empty():
    c = q.get()
    if g.safe_get(c) != 1:
      continue
    if not is_accessible(g, c):
      continue

    # Remove the roll
    g.safe_set(c, 0)

    # add neighbors to queue
    neighbors = g.get_neighbors(c, grid.ortho_diag_neighbors)
    for n, val in neighbors:
      if val == 1:
        q.put(n)

    # Udpate total
    total_removed += 1

  # print(g.str_dot_hash())
  print(total_removed)
  

part2()

