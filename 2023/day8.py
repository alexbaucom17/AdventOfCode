import sys
sys.path.append('.')
import aoc
import math
import numpy as np

data_rows = aoc.get_input(8, sample=False, index=2).splitlines()

def parse_inputs():
  int_steps = ["LR".index(char) for char in data_rows[0]]
  nodes = {}
  for row in data_rows[2:]:
    fixed_row = row.replace("=", "").replace("(", "").replace(")", "").replace(",", "")
    key, left_val, right_val = fixed_row.split()
    nodes[key] = (left_val, right_val)
  return int_steps, nodes

def part1():
  steps, nodes = parse_inputs()
  cur_node = "AAA"
  num_steps = 0
  while cur_node != "ZZZ":
    next_step = steps[num_steps % len(steps)]
    cur_node = nodes[cur_node][next_step]
    num_steps += 1
  print(num_steps)

# part1()

def preprocess_nodes(nodes, steps):
  node_map = {}
  for node in nodes.keys():
    cur_node = node
    end_zs = set()
    if cur_node[-1] == "Z":
      end_zs.add(0)
    for ix, step in enumerate(steps):
      cur_node = nodes[cur_node][step]
      if cur_node[-1] == "Z":
        end_zs.add(ix+1)
    node_map[node] = (cur_node, end_zs)
  return node_map

def find_cycles(node_map):
  cycle_map = {}
  for node in node_map.keys():
    cur_node = node
    explored = []
    while cur_node not in explored:
      explored.append(cur_node)
      cur_node = node_map[cur_node][0]

    cycle_node = cur_node
    cycle_ix = explored.index(cur_node)
    explored.append(cur_node)
    pre_cycle = explored[0:cycle_ix]
    cycle = explored[cycle_ix:-1]
    cycle_map[node] = (cycle_node, pre_cycle, cycle)
  return cycle_map

def get_step_counts(cycle_map, num_steps, node_map):
  step_counts = {}
  for node in cycle_map.keys():
    pre_cycle_steps = len(cycle_map[node][1])*num_steps
    cycle = cycle_map[node][2]
    cycle_steps = len(cycle)*num_steps
    cycle_z_steps = set()
    for i,cycle_node in enumerate(cycle):
      z_steps = node_map[cycle_node][1]
      for z_step in z_steps:
        cycle_z_steps.add((i*num_steps + z_step) % cycle_steps)
    step_counts[node] = (pre_cycle_steps, cycle_steps, cycle_z_steps)
  return step_counts

def part2():
  steps, nodes = parse_inputs()
  cur_nodes = [n for n in nodes.keys() if n[-1] == "A"]
  num_steps = 0
  print(cur_nodes)
  while not all([n[-1] == "Z" for n in cur_nodes]):
    if num_steps % 1000000 == 0:
      print(f"steps: {num_steps}, num_zs: {sum([n[-1] == 'Z' for n in cur_nodes])}")

    next_step = steps[num_steps % len(steps)]
    for i in range(len(cur_nodes)):
      cur_nodes[i] = nodes[cur_nodes[i]][next_step]
    num_steps += 1
    # print(cur_nodes)
  print(num_steps)

def part2_v2():
  steps, nodes = parse_inputs()
  node_map = preprocess_nodes(nodes, steps)
  cycle_map = find_cycles(node_map)
  step_counts = get_step_counts(cycle_map, len(steps), node_map)
  # print("node_map")
  # print(node_map)
  # print("cycle_map")
  # print(cycle_map)
  # print("step_counts")
  # print(step_counts)

  starting_nodes = [n for n in nodes.keys() if n[-1] == "A"]
  relevant_cycle_starts = {n: cycle_map[n][1] for n in starting_nodes}
  print(relevant_cycle_starts)
  relevant_step_counts = {n: step_counts[n] for n in starting_nodes}
  print("relevant_step_counts")
  print(relevant_step_counts)
  step_counts_64 = np.asarray([cycle_info[1] for cycle_info in relevant_step_counts.values()], dtype=np.uint64)
  lcm_cycle_steps = int(np.lcm.reduce(step_counts_64))
  print(f"lcm steps: {lcm_cycle_steps}")
  

  test_node = list(relevant_step_counts.values())[0]
  print(test_node)
  test_offset = test_node[0] + test_node[2].pop()
  
  loops = 1000000000
  for i in range(loops):
    total_steps = test_offset + i*test_node[1] 
    if i % 1000000 == 0:
      print(f"{i}/{loops} - testing {total_steps}")

    all_valid = True
    for validate_node in list(relevant_step_counts.values())[1:]:
      valid_offset = False
      for o in validate_node[2]:
        if (total_steps - o - validate_node[0]) % validate_node[1] == 0:
          valid_offset = True
      if not valid_offset:
        all_valid = False
        continue

    if all_valid:
      print(total_steps)
      break


    # steps = lcm_cycle_steps * i
    # all_matches = []
    # for node in relevant_step_counts.values():
    #   node_matchs = set([node[0] + steps + z_step for z_step in node[2]])
    #   all_matches.append(node_matchs)
    # print(all_matches)
    # intersect = set.intersection(*all_matches)
    # if intersect:
    #   print(intersect)

part2_v2()


"""
Find s
c1*a1 + o1 = s -> a1 = (s-o1)/c1 -> a1 and s must be integers
c2*a2 + o2 = s
c3*a3 + o3 = s

"""