import sys
sys.path.append('.')
import aoc
import math
from dataclasses import dataclass, field
import re
import copy
from operator import itemgetter
from collections import defaultdict
import time

data_rows = aoc.get_input(16, sample=True, index=0).splitlines()

@dataclass()
class Step:
  id: str
  dist: int

@dataclass()
class Node:
  id: str
  connected: list[Step]
  flow: int

def parse_input(rows) -> dict[Node]:
  all_nodes = {}
  for row in rows:
    flow = int(re.findall("[0-9]+", row)[0])
    id = re.findall("Valve [A-Z]+ has", row)[0].split()[1]
    words = row.split()
    connected = []
    for i in range(len(words)-1, 0 , -1):
      if words[i] in ["valves", "valve"]:
        break
      else:
        connected.append(words[i].replace(",",""))
    
    all_nodes[id] = Node(id, [Step(x, 1) for x in connected], flow)

  return all_nodes

def merge_node(prune_node: Node, keep_node: Node) -> Node:

  prune_to_keep_dist = None

  prune_node_other_connections = []
  for step in prune_node.connected:
    if step.id != keep_node.id:
      prune_node_other_connections.append(step)
    else:
      prune_to_keep_dist = step.dist

  keep_node_other_connections = []
  for step in keep_node.connected:
    if step.id != prune_node.id:
      keep_node_other_connections.append(step)

  prune_node_other_connections = [Step(x.id, x.dist+prune_to_keep_dist) for x in prune_node_other_connections]
  all_connections = prune_node_other_connections + keep_node_other_connections
  return Node(keep_node.id, all_connections, keep_node.flow)


def simplify_graph(nodes: dict[Node], start_id: str):
  ids_to_prune = set()
  for id, node in nodes.items():
    # Don't prune starting id
    if id == start_id:
      continue

    # Don't prune anything with nonzero flow
    if node.flow > 0:
      continue

    # At this point, we have a node with 0 flow to prune
    ids_to_prune.add(id)

    for step in node.connected:
      nodes[step.id] = merge_node(node, nodes[step.id])
  
  for id in ids_to_prune:
    del nodes[id]

@dataclass(frozen=True, eq=True)
class PathState:
  id: str
  time: int
  pressure: int
  visited: defaultdict[int] = field(compare=False)
  opened: frozenset[str]

def compute_step_score(s1: PathState, s2: PathState, max_steps: int) -> int:
  p = s1.pressure
  if s2.time > max_steps:
    dt = max_steps + 1 - s1.time
  else:
    dt = s2.time - s1.time
  return p * dt

def compute_path_score(path: list[PathState], max_steps: int) -> int:
  total = 0
  for i in range(len(path) - 1):
    total += compute_step_score(path[i], path[i+1],max_steps)

  # Path may end before MAX_STEPS if all valves are open
  if path[-1].time <= max_steps:
    total += path[-1].pressure * (max_steps + 1 - path[-1].time)
  
  return total

def all_valves_open(nodes: dict[Node], opened_ids: set[str]) -> bool:
  valve_ids = set([n.id for n in nodes.values() if n.flow > 0])
  return opened_ids == valve_ids

def find_path_helper(nodes: dict[Node], cur_state: PathState, cache: dict, cache_stats: dict, max_steps: int) -> tuple[list[PathState], int]:
  
  # If the current state is cached, use it
  if cur_state in cache:
    cache_stats["hit"] += 1
    end_path, end_score = cache[cur_state]
    return end_path, end_score
  else:
    cache_stats["miss"] += 1

  # If the current state has too large of a time, this state is the end of a path
  if cur_state.time > max_steps:
    path = []
    score = 0
    cache[cur_state] = (path, score)
    return (path, score)
  
  # If all valves are opened in this state, we can end the path
  if all_valves_open(nodes, cur_state.opened):
    path = [cur_state]
    score = compute_path_score(path, max_steps)
    cache[cur_state] = (path, score)
    return (path, score)

  # Now, explore actions we can take at this state
  candidate_paths = []
  cur_id = cur_state.id

  # To open current valve
  if nodes[cur_id].flow > 0 and cur_id not in cur_state.opened:
    new_visited = copy.copy(cur_state.visited)
    new_opened = set(copy.copy(cur_state.opened))
    new_opened.add(cur_id)
    next_state = PathState(
      id=cur_id,
      time=cur_state.time + 1,
      pressure=cur_state.pressure + nodes[cur_id].flow,
      visited=new_visited,
      opened=frozenset(new_opened))

    path, score = find_path_helper(nodes, next_state, cache, cache_stats, max_steps)
    candidate_paths.append((path, score))
    
  # To walk to next nodes
  for step in nodes[cur_id].connected:

    # if cur_state.visited[step.id] >= MAX_VISITS:
    #   continue

    new_visited = copy.copy(cur_state.visited)
    new_visited[step.id] += 1
    new_opened = copy.copy(cur_state.opened)
    next_state = PathState(
      id=step.id,
      time=cur_state.time + step.dist,
      pressure=cur_state.pressure,
      visited=new_visited,
      opened=new_opened)

    path, score = find_path_helper(nodes, next_state, cache, cache_stats, max_steps)
    candidate_paths.append((path, score))

  # debug_states = [("AA", 1, -1), ("BB",3, -1), ("DD",3, -1)]
  # for id, t, p in debug_states:
  #   if cur_id == id and cur_state.time == t and cur_state.pressure > p:
  #     print(cur_state)
  #     for path, score in candidate_paths:
  #       l = [(p.id, p.time) for p in path]
  #       print(f"{score}: {l}")

  ret_path = None
  ret_score = 0
  if candidate_paths:
    # If we had actions available to take, pick the best action to maximize score
    for path, score in candidate_paths:
      if path:
        new_score = compute_step_score(cur_state, path[0], max_steps) + score
        new_path = [cur_state] + path
      else:
        new_path = [cur_state]
        new_score = compute_path_score(new_path, max_steps)
      
      if new_score > ret_score:
        ret_score = new_score
        ret_path = new_path

  else:
    # If not actions were available, this is the end of a path
    ret_path = [cur_state]
    ret_score = compute_path_score(ret_path, max_steps)

  # Add to the cache and return
  cache[cur_state] = (ret_path, ret_score)
  return (ret_path, ret_score)


def find_all_paths(nodes: dict[Node], start_id: str, max_steps: int):
  visited = defaultdict(int)
  visited[start_id] += 1
  cur_state = PathState(id=start_id, time=1, pressure=0, visited=visited, opened=frozenset())

  cache = {}
  cache_stats = {"hit": 0, "miss": 0}

  best_path, score = find_path_helper(nodes, cur_state, cache, cache_stats, max_steps)
  for path in best_path:
    print(f"{path.id}: t={path.time}, p={path.pressure}, open={path.opened}")
  print(score)
  print(f"Cache stats - hit:{cache_stats['hit']}, miss: {cache_stats['miss']}, percent: {cache_stats['hit']/(cache_stats['hit'] + cache_stats['miss']):.1%}")

  # print("Cache")
  # for k,v in cache.items():
  #   print(f"{k.id}: t={k.time}, p={k.pressure}, open={k.opened}")
  #   print(f"  {v[1]}")
  #   print(f"  {[(p.id, p.time) for p in v[0]]}")


def part1():
  start_id = "AA"
  max_steps = 30
  all_nodes = parse_input(data_rows)

  print("all nodes")
  for n in all_nodes.values():
    print(n)
  
  simplify_graph(all_nodes, start_id)
  print("Simplified nodes")
  for n in all_nodes.values():
    print(n)

  t_start = time.time()
  find_all_paths(all_nodes, start_id, max_steps)
  print(f"Time taken: {time.time() - t_start}")
  
# part1()


@dataclass(frozen=True, eq=True)
class PathState2:
  id: str
  id_e: str
  time: int
  opened_id: int

def compute_step_score2(s1: PathState2, s2: PathState2, max_steps: int, opened_cache: dict) -> int:
  p = opened_cache[s1.opened_id][0]
  if s2.time > max_steps:
    dt = max_steps + 1 - s1.time
  else:
    dt = s2.time - s1.time
  return p * dt

def compute_path_score2(path: list[PathState2], max_steps: int, opened_cache: dict) -> int:
  total = 0
  for i in range(len(path) - 1):
    total += compute_step_score2(path[i], path[i+1], max_steps, opened_cache)

  # Path may end before MAX_STEPS if all valves are open
  if path[-1].time <= max_steps:
    total += opened_cache[path[-1].opened_id][0] * (max_steps + 1 - path[-1].time)
  
  return total

def generate_next_states2(nodes: dict[Node], cur_state: PathState2, opened_cache: dict) -> list[PathState2]:
  my_actions = []
  my_id = cur_state.id
  if nodes[my_id].flow > 0 and my_id not in opened_cache[cur_state.opened_id][1]:
    my_actions.append("open")
  for step in nodes[my_id].connected:
    my_actions.append(step.id)
  
  e_actions = []
  e_id = cur_state.id_e
  if nodes[e_id].flow > 0 and e_id not in opened_cache[cur_state.opened_id][1]:
    e_actions.append("open")
  for step in nodes[e_id].connected:
    e_actions.append(step.id)

  states = []
  for m_a in my_actions:
    for e_a in e_actions:
      my_id_new = my_id
      e_id_new = e_id
      new_opened_id = cur_state.opened_id
      new_pressure, cur_opened = opened_cache[new_opened_id]
      new_opened = set(copy.copy(cur_opened))
      update_opened = False

      if m_a == "open":
        if my_id not in new_opened:
          new_opened.add(my_id)
          new_pressure += nodes[my_id].flow
          update_opened = True
      else:
        my_id_new = m_a
      
      if e_a == "open":
        if e_id not in new_opened:
          new_opened.add(e_id)
          new_pressure += nodes[e_id].flow
          update_opened = True
      else:
        e_id_new = e_a

      if update_opened:
        opened_entry = (new_pressure, frozenset(new_opened))
        found = False
        for k,v in opened_cache.items():
          if v[1] == opened_entry[1]:
            new_opened_id = k
            found = True
            break
        if not found:
          new_opened_id = max(opened_cache.keys()) + 1
          opened_cache[new_opened_id] = opened_entry


      states.append(PathState2(
        id=my_id_new,
        id_e=e_id_new,
        time=cur_state.time + 1,
        opened_id=new_opened_id
      ))

  return states
      

def find_path_helper2(nodes: dict[Node], cur_state: PathState2, cache: dict, cache_stats: dict, max_steps: int, opened_cache: dict) -> tuple[list[PathState2], int]:
  
  # If the current state is cached, use it
  if cur_state in cache:
    cache_stats["hit"] += 1
    end_path, end_score = cache[cur_state]
    return end_path, end_score
  else:
    cache_stats["miss"] += 1

  # If the current state has too large of a time, this state is the end of a path
  if cur_state.time > max_steps:
    path = []
    score = 0
    cache[cur_state] = (path, score)
    return (path, score)
  
  # If all valves are opened in this state, we can end the path
  if all_valves_open(nodes, opened_cache[cur_state.opened_id][1]):
    path = [cur_state]
    score = compute_path_score2(path, max_steps, opened_cache)
    cache[cur_state] = (path, score)
    return (path, score)

  # Now, explore actions we can take at this state
  candidate_paths = []
  next_states = generate_next_states2(nodes, cur_state, opened_cache)
  for next_state in next_states:
    path, score = find_path_helper2(nodes, next_state, cache, cache_stats, max_steps, opened_cache)
    candidate_paths.append((path, score))

  # Now score and select best next state
  ret_path = None
  ret_score = 0
  if candidate_paths:
    # If we had actions available to take, pick the best action to maximize score
    for path, score in candidate_paths:
      if path:
        new_score = compute_step_score2(cur_state, path[0], max_steps, opened_cache) + score
        new_path = [cur_state] + path
      else:
        new_path = [cur_state]
        new_score = compute_path_score2(new_path, max_steps, opened_cache)
      
      if new_score > ret_score:
        ret_score = new_score
        ret_path = new_path

  else:
    # If not actions were available, this is the end of a path
    ret_path = [cur_state]
    ret_score = compute_path_score2(ret_path, max_steps, opened_cache)

  # Add to the cache and return
  cache[cur_state] = (ret_path, ret_score)
  return (ret_path, ret_score)

def find_all_paths2(nodes: dict[Node], start_id: str, max_steps: int):
  cur_state = PathState2(id=start_id, id_e=start_id, time=1, opened_id=0)

  cache = {}
  cache_stats = {"hit": 0, "miss": 0}
  opened_cache = {0: (0, frozenset())}

  best_path, score = find_path_helper2(nodes, cur_state, cache, cache_stats, max_steps, opened_cache)
  for path in best_path:
    print(f"{path.id},{path.id_e}: t={path.time}, p={opened_cache[path.opened_id][0]}, open={opened_cache[path.opened_id][1]}")
  print(score)
  print(f"Cache stats - hit:{cache_stats['hit']}, miss: {cache_stats['miss']}, percent: {cache_stats['hit']/(cache_stats['hit'] + cache_stats['miss']):.1%}")


def part2():
  start_id = "AA"
  max_steps = 26
  all_nodes = parse_input(data_rows)

  t_start = time.time()
  find_all_paths2(all_nodes, start_id, max_steps)
  print(f"Time taken: {time.time() - t_start}")

part2()