import sys
sys.path.append('.')
import aoc
import math
from typing import Any, List

data_rows = aoc.get_input(7, sample=False, index=0).splitlines()

class Node:
  parent: Any
  root: bool
  name: str
  id: int

  def __init__(self, id: int, name: str, parent: Any, root:bool=False):
    self.parent = parent
    self.root = root
    self.name = name
    self.id = id

  def get_size(self) -> int:
    raise NotImplementedError("Not implemented")

class Dir(Node):
  children: List[Any]

  def __init__(self, id: int, name: str, parent: Any, root: bool=False):
    super().__init__(id, name, parent, root)
    self.children = []

  def add_child(self, child: Node):
    self.children.append(child)

  def get_size(self) -> int:
    return sum([child.get_size() for child in self.children])

  def get_children_nested(self, cur_nest):
    ret = []
    for child in self.children:
      ret.append((cur_nest, child))
      if type(child) == Dir:
        ret += child.get_children_nested(cur_nest+1)
    return ret

  def __str__(self):
    return f"{self.name} (dir)"

class File(Node):
  size: int

  def __init__(self, id: int, name: str, parent: Any, size: int):
    super().__init__(id, name, parent)
    self.size = size

  def get_size(self) -> int:
    return self.size

  def __str__(self):
    return f"{self.name} (file, size={self.size})"

class DirTree:
  
  def __init__(self):
    self.nodes = [Dir(0, "/", None, root=True)]

  def get_node(self, id: int) -> Node:
    for node in self.nodes:
      if node.id == id:
        return node
    raise ValueError(f"Could not find node: {id}")

  def add_dir(self, name: str, parent_id: int):
    # print(f"Adding dir: {name} to directory: {parent_name}")
    parent_node = self.get_node(parent_id)
    assert type(parent_node) == Dir
    self.nodes.append(Dir(len(self.nodes), name, parent_node))
    parent_node.add_child(self.nodes[-1])

  def add_file(self, name: str, size: int, parent_id: int):
    # print(f"Adding file: {name} to directory: {parent_name}")
    parent_node = self.get_node(parent_id)
    assert type(parent_node) == Dir
    self.nodes.append(File(len(self.nodes), name, parent_node, size))
    parent_node.add_child(self.nodes[-1])

  def print(self):
    nested_nodes = self.nodes[0].get_children_nested(1)
    print(self.nodes[0])
    for nesting, node in nested_nodes:
      prefix = "  " * nesting
      print(prefix + "- " + str(node))

  def get_dir_sizes(self):
    sizes = []
    for node in self.nodes:
      if type(node) == Dir:
        sizes.append((node.name, node.get_size()))
    return sizes


def find_command_lines(lines):
  command_lines = []
  for i in range(len(lines)):
    if lines[i][0] == '$':
      command_lines.append(i)
  return command_lines + [len(lines)]

def create_directory_from_commands(lines, command_lines) -> DirTree:
  cur_dir_id = None
  tree = DirTree()
  for i in range(len(command_lines) - 1):
    cur_command_idx = command_lines[i]
    command_tokens = lines[cur_command_idx].split()
    if command_tokens[1] == 'cd':
      if command_tokens[2] == "/":
        cur_dir_id = 0
        # print("To dir /")
      elif command_tokens[2] == "..":
        cur_dir_id = tree.get_node(cur_dir_id).parent.id
        # print(f"Moving up to dir {cur_dir_id}")
      else:
        child_nodes = tree.get_node(cur_dir_id).children
        dir_name = command_tokens[2]
        found = False
        for node in child_nodes:
          if dir_name == node.name:
            found = True
            cur_dir_id = node.id
        if not found:
          tree.print()
          raise ValueError(f"Could not find dir {dir_name} in {[str(node) for node in child_nodes]}")
        # print(f"Moving down to dir {cur_dir_id}")
    elif command_tokens[1] == "ls":
      next_command_idx = command_lines[i+1]
      for j in range(cur_command_idx+1, next_command_idx):
        line_tokens = lines[j].split()
        if line_tokens[0] == "dir":
          tree.add_dir(line_tokens[1], cur_dir_id)
        else:
          tree.add_file(line_tokens[1], int(line_tokens[0]), cur_dir_id)
    else:
      raise ValueError(f"Unknown command: {command_tokens}")
  return tree
   

def part1():
  command_lines = find_command_lines(data_rows)
  tree = create_directory_from_commands(data_rows, command_lines)
  # tree.print()
  sizes = tree.get_dir_sizes()
  total = 0
  for name, size in sizes:
    if size <= 100000:
      total += size
  print(total)
  

# part1()

def part2():
  command_lines = find_command_lines(data_rows)
  tree = create_directory_from_commands(data_rows, command_lines)
  # tree.print()
  sizes = tree.get_dir_sizes()
  max_size = 70000000
  req_free = 30000000
  cur_free = max_size - sizes[0][1]
  size_needed = req_free - cur_free
  min_size_to_delete = max_size
  for name, size in sizes:
    if size > size_needed and size < min_size_to_delete:
      min_size_to_delete = size
  print(min_size_to_delete)


part2()