import sys
sys.path.append('.')
import aoc
import math
import dataclasses
import queue
from typing import Optional

data_rows = aoc.get_input(10, sample=False, index=5).splitlines()

@dataclasses.dataclass(frozen=True, eq=True)
class Location:
  row: int
  col: int
  dir: str = dataclasses.field(hash=False)

pipes_dirs = {
  "|": "ns",
  "-": "ew",
  "L": "ne",
  "J": "nw",
  "7": "sw",
  "F": "se",
  ".": "",
  "S": ""
}

dir_steps = {
  "n": [-1, 0],
  "s": [1, 0],
  "e": [0, 1],
  "w": [0, -1]
}

flip = {
  "n": "s",
  "s": "n",
  "e": "w",
  "w": "e"
}

pipes_dirs_left = {
  "|": {"n": "w", "s": "e"},
  "-": {"e": "n", "w": "s"},
  "L": {"n": "ws", "e": ""},
  "J": {"n": "", "w": "es"},
  "7": {"w": "", "s": "en"},
  "F": {"s": "", "e": "nw"},
  ".": {},
  "S": {}
}

def get_pipe(loc: Location, grid: list[list[str]]) -> str:
  return grid[loc.row][loc.col]

def walk(loc: Location, grid: list[list[str]]) -> Location:
  cur_pipe = get_pipe(loc, grid)
  if cur_pipe != "S":
    connections = pipes_dirs[cur_pipe]
    new_dir = [d for d in connections if flip[d] != loc.dir]
    if len(new_dir) != 1:
      raise ValueError(f"Found new_dirs: {new_dir} from cur_pipe: {cur_pipe} and connections: {connections}")
    new_step = dir_steps[new_dir[0]]
  else:
    new_dir = "q"
  return Location(
    row=loc.row + new_step[0],
    col=loc.col + new_step[1],
    dir=new_dir[0]
  )

def find_start(grid: list[list[str]]) -> Location:
  for rx, row in enumerate(grid):
    for cx, char in enumerate(row):
      if char == "S":
        for dir, step in dir_steps.items():
          new_rx = rx + step[0]
          new_cx = cx + step[1]
          adj_pipe = get_pipe(Location(new_rx, new_cx, ""), grid)
          if flip[dir] in pipes_dirs[adj_pipe]:
            return Location(row=new_rx, col=new_cx, dir=dir)
        raise ValueError(f"Could not find valid dir for starting location {rx}, {cx}")
  raise ValueError("Could not find starting location")

def part1():
  cur_loc = find_start(data_rows) 
  num_steps = 1
  while get_pipe(cur_loc, data_rows) != "S":
    # print(f"{cur_loc}, pipe: {get_pipe(cur_loc, data_rows)}")
    cur_loc = walk(cur_loc, data_rows)
    num_steps += 1
  print(num_steps/2)

# part1()

def get_new_loc(loc: Location, dir: str, grid: list[list[str]], path_set: set[tuple[int, int]]) -> Optional[Location]:
  new_step = dir_steps[dir]
  new_loc = Location(
    row=loc.row + new_step[0],
    col=loc.col + new_step[1],
    dir="q"
  )
  if new_loc.row >= 0 and new_loc.col >= 0 and new_loc.row < len(grid) and new_loc.col < len(grid[0]) and (new_loc.row, new_loc.col) not in path_set:
    return new_loc
  return None

def get_partitions(path: list[Location], grid: list[list[str]]) -> tuple[set[Location], set[Location]]:
  lefts = set()
  rights = set()
  path_set = set([(loc.row, loc.col) for loc in path])

  for loc in path:
    char = get_pipe(loc, grid)
    if char == "S":
      continue
    side_dirs = pipes_dirs_left[char]
    left_dirs = side_dirs[flip[loc.dir]]
    right_dirs = [s for d, s in side_dirs.items() if d != flip[loc.dir]]
    if len(right_dirs) != 1:
      raise ValueError(f"Invalid computation for right_dirs {right_dirs} from sides: {side_dirs} with at loc: {loc}")
    right_dirs = right_dirs[0]

    # print(f"loc: {loc}, char: {char}, side_dirs: {side_dirs}, left_dirs: {left_dirs}, right_dirs: {right_dirs}")

    for new_dir in left_dirs:
      new_loc = get_new_loc(loc, new_dir, grid, path_set)
      if new_loc:
        lefts.add(new_loc)
    for new_dir in right_dirs:
      new_loc = get_new_loc(loc, new_dir, grid, path_set)
      if new_loc:
        rights.add(new_loc)
  return lefts, rights

def draw(grid: list[list[str]], path: list[Location], lefts: set[Location], rights: set[Location]):
  new_grid = [["." for c in r] for r in grid]
  for p in path:
    new_grid[p.row][p.col] = "p"
  for l in lefts:
    new_grid[l.row][l.col] = "L"
  for r in rights:
    new_grid[r.row][r.col] = "R"

  for r in new_grid:
    print("".join(r))

def join_partitions(grid: list[list[str]], path: list[Location], lefts: set[Location], rights: set[Location]):
  not_checked = set()
  path_set = set([(loc.row, loc.col) for loc in path])
  for rx in range(len(grid)):
    for cx in range(len(grid[rx])):
      test_loc = Location(rx, cx, "q")
      if (test_loc.row, test_loc.col) not in path_set and test_loc not in lefts and test_loc not in rights:
        not_checked.add(test_loc)

  print(f"not_checked num: {len(not_checked)}")

  for loc in not_checked:
    q = queue.Queue()
    q.put(loc)
    explored = set()
    while q:
      check_loc = q.get()
      if (check_loc.row, check_loc.col) in path_set:
        continue
      if check_loc in lefts:
        lefts.add(loc)
        break
      if check_loc in rights:
        rights.add(loc)
        break
      if check_loc in explored:
        continue
      explored.add(check_loc)
      for new_step in dir_steps.keys():
        new_loc = get_new_loc(check_loc, new_step, grid, path_set)
        if new_loc:
          q.put(new_loc)

def part2():
  cur_loc = find_start(data_rows)
  path = [cur_loc]
  while get_pipe(cur_loc, data_rows) != "S":
    # print(f"{cur_loc}, pipe: {get_pipe(cur_loc, data_rows)}")
    cur_loc = walk(cur_loc, data_rows)
    path.append(cur_loc)

  print(f"Done with loop finding. Size: {len(path)}")
  lefts, rights = get_partitions(path, data_rows)
  print(f"Found partitions. Left: {len(lefts)}, right: {len(rights)}")
  # draw(data_rows, path, lefts, rights)
  join_partitions(data_rows, path, lefts, rights)
  print(f"Joined partitions. Left: {len(lefts)}, right: {len(rights)}")
  # print("-----------")
  draw(data_rows, path, lefts, rights)
  print(f"lefts: {len(lefts)}")
  print(f"rights: {len(rights)}")


part2()