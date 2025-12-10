
import sys
sys.path.append('.')
import aoc
from aoc_utils import parsing
import dataclasses
import queue
import copy
import numpy as np
import cvxpy as cp

data_rows = aoc.get_input(day=10, sample=False, index=0).splitlines()

@dataclasses.dataclass(frozen=True)
class Machine:
  goal: tuple[bool, ...]
  buttons: tuple[tuple[int, ...], ...]
  joltage: tuple[int, ...]

def parse(data_rows: list[str]) -> list[Machine]:
  machines = []
  for row in data_rows:
    groups = row.split(" ")
    goal_str = groups[0]
    buttons_strs = groups[1:-1]
    joltage_str = groups[-1]
    goal = tuple(c == '#' for c in goal_str[1:-1])
    buttons = []
    for s in buttons_strs:
      buttons.append(tuple(int(c) for c in s[1:-1].split(',')))
    joltage = tuple(int(c) for c in joltage_str[1:-1].split(','))
    machines.append(Machine(goal, buttons, joltage))
  return machines

def find_min_initialization(m: Machine) -> list[tuple[int]]:
  # queue holds (light_state, button_sequence)
  q = queue.Queue()
  init_state = tuple(False for i in range(len(m.goal)))
  q.put((init_state, []))
  
  # visited holds light_state - since this is bfs we can skip anything we have visited before knowing
  # we previously saw it on a shorter path.
  visited = set()

  button_updates = []
  for button in m.buttons:
    button_updates.append([i in button for i in range(len(init_state))])

  while not q.empty():
    state, path = q.get()
    if state == m.goal:
      return path
    
    if state in visited:
      continue
    
    visited.add(state)

    for update in button_updates:
      new_state = tuple(a ^ b for a, b in zip(update, state))
      new_path = copy.deepcopy(path)
      new_path.append(update)
      q.put((new_state, new_path))
    

  raise ValueError("No solution found")


def part1():
  total = 0
  machines = parse(data_rows)
  print(f"Num machines: {len(machines)}")
  for i, m in enumerate(machines):
    # print(m)
    min_path = find_min_initialization(m)
    # print(min_path)
    # print(len(min_path))
    print(f"Solved {i}, found path of length {len(min_path)}")
    total += len(min_path)
  print(total)

# part1()

def dist(goal, state) -> int:
  return np.sum(np.abs(goal-state))


def find_min_joltage(m: Machine) -> int:
  # queue holds (joltage_state, path_length)
  q = queue.PriorityQueue()
  target = np.asarray(m.joltage)
  init_state = np.zeros_like(target)
  initial_dist = int(dist(target, init_state))
  q.put((initial_dist, (init_state, 0)))
  
  # visited holds joltage_state - since this is bfs we can skip anything we have visited before knowing
  # we previously saw it on a shorter path.
  visited = set()

  button_updates = []
  for button in m.buttons:
    button_updates.append(np.asarray([int(i in button) for i in range(len(init_state))]))

  while not q.empty():
    _, data = q.get()
    state, path_length = data
    state = np.asarray(state)
    if np.all(state == target):
      print(f"Visited size: {len(visited)}")
      return path_length
    
    if tuple(state) in visited:
      continue
    
    visited.add(tuple(state))

    for update in button_updates:
      for mult in [1, 2]:
        new_state = state + mult * update
        if tuple(new_state) in visited:
          continue
        if np.any(state > target):
          continue
        new_dist = int(dist(target, new_state))
        q.put((int(new_dist+path_length+mult), (tuple(new_state), int(path_length+mult))))

  raise ValueError("No solution found")

def find_min_joltage_opt(m: Machine) -> int:
  n_buttons = len(m.buttons)
  n_targets = len(m.joltage)
  A = np.zeros((n_targets, n_buttons), dtype=np.int16)
  for b_ix, buttons in enumerate(m.buttons):
    for target_ix in buttons:
      A[target_ix, b_ix] = 1
  b = np.asarray(m.joltage, dtype=np.int16)

  x = cp.Variable(n_buttons, integer=True)
  objective = cp.Minimize(cp.sum(x))
  constraints = [0 <= x, A @ x == b]

  prob = cp.Problem(objective, constraints)

  result = prob.solve()
  return int(result)


def part2():
  total = 0
  machines = parse(data_rows)
  print(f"Num machines: {len(machines)}")
  for i, m in enumerate(machines):
    min_path_len = find_min_joltage_opt(m)
    # print(min_path)
    # print(len(min_path))
    print(f"Solved {i}, found path of length {min_path_len}")
    total += min_path_len
  print(total)

"""
What do we know
a[0] * button[0] + a[1] * button[1] ... = target
This gives K_targets equations for N_button variables
want: min(sum(a[..., N_buttons]))
button press order doesn't matter any more - so a proper ordered search isn't necessary

"""

part2()

