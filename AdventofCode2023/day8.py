import sys
sys.path.append('.')
import aoc
import math

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
  cur_nodes = [n for n in nodes.keys() if n[-1] == "A"]
  num_steps = 0
  while True:
    if num_steps % 1000000 == 0:
      print(f"steps: {num_steps*len(steps)}")

    end_zs = node_map[cur_nodes[0]][1]
    for node in cur_nodes[1:]:
      end_zs = end_zs & node_map[node][1]
      if not end_zs:
        break
    if end_zs:
      print(num_steps * len(steps) + end_zs.pop())
      break

    for i in range(len(cur_nodes)):
      cur_nodes[i] = node_map[cur_nodes[i]][0]
    num_steps += 1

# Ideas to try
# Find all sets of nodes which could possibly be end conditions
#   Get all end_z steps possible and then find all groups that have those values
#   Use this for quicker end check in each loop rather than the set unions
# Make/find some other test inputs to validate that I don't have an infinite loop bug?
# Figure out if there is some mathematical way to do the node mapping so I can just calculate the number of steps rather than simulating them

part2_v2()