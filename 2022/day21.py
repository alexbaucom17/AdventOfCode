import sys
sys.path.append('.')
import aoc
import math
from dataclasses import dataclass
from typing import Optional

data_rows = aoc.get_input(21, sample=False, index=0).splitlines()

@dataclass
class Node:
  id: str
  num: Optional[int] = None
  node1: Optional[str] = None
  node2: Optional[str] = None
  op: Optional[str] = None

def parse_node(line):
  id, other = line.split(":")
  other_split = other.strip().split(" ")

  if len(other_split) == 1:
    num = int(other_split[0])
    return Node(id, num)
  elif len(other_split) == 3:
    return Node(id, node1=other_split[0], op=other_split[1], node2=other_split[2])
  else:
    raise ValueError(F"Invalid other split: {other_split}")

def eval_node(data, node_id):

  node = data[node_id]
  if node.num is not None:
    return node.num
  else:
    v1 = eval_node(data, node.node1)
    v2 = eval_node(data, node.node2)
    if node.op == "+":
      val = v1 + v2
    elif node.op == "-":
      val = v1 - v2
    elif node.op == "*":
      val = v1 * v2
    elif node.op == "/":
      val = int(v1 / v2)
    else:
      raise ValueError(f"Unsupported op: {node.op}")
    data[node_id].num = val
    return val

def inverse_op1(op, v2, answer):
    if op == "+":
      return answer - v2
    elif op == "-":
      return answer + v2
    elif op == "*":
      return int(answer / v2)
    elif op == "/":
      return answer * v2
    else:
      raise ValueError(f"Unsupported op: {op}")

def inverse_op2(op, v1, answer):
    if op == "+":
      return answer - v1
    elif op == "-":
      return v1 - answer
    elif op == "*":
      return int(answer / v1)
    elif op == "/":
      return int(v1 / answer)
    else:
      raise ValueError(f"Unsupported op: {op}")

def eval_inverse(data, node_id, answer):
  if node_id == "humn":
    print(f"humn: {answer}")

  v1 = None
  v2 = None
  try:
    v1 = eval_node(data, data[node_id].node1)
  except KeyError:
    pass
  try:
    v2 = eval_node(data, data[node_id].node2)
  except KeyError:
    pass

  if v1 is None and v2 is not None:
    v1_answer = inverse_op1(data[node_id].op, v2, answer)
    eval_inverse(data, data[node_id].node1, v1_answer)
  elif v2 is None and v1 is not None:
    v2_answer = inverse_op2(data[node_id].op, v1, answer)
    eval_inverse(data, data[node_id].node2, v2_answer)

def part1():
  data = {}
  for line in data_rows:
    node = parse_node(line)
    data[node.id] = node

  print(eval_node(data, "root"))

# part1()

def part2():
  data = {}
  for line in data_rows:
    node = parse_node(line)
    data[node.id] = node
    
  data["humn"].num = None
  root_known = eval_node(data, data["root"].node2)
  root_unknown_side = data["root"].node1
  eval_inverse(data, root_unknown_side, root_known)

part2()