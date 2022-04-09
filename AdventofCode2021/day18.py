from audioop import lin2adpcm
import sys
from turtle import down, left

from numpy import isin
sys.path.append('.')
import aoc
import math
from dataclasses import dataclass
from enum import Enum

data_rows = aoc.get_input(18, sample=False, index=4).splitlines()

class Side(Enum):
    LEFT = 0
    RIGHT = 1

class Dir(Enum):
    UP = 0
    DOWN = 1

@dataclass
class Node:
    parent_index: int
    parent_side: Side

    def is_root(self):
        return self.parent_index == -1

    def shift_index(self, shift: int): 
        self.parent_index += shift

@dataclass
class Leaf(Node):
    value: int

@dataclass
class Branch(Node):
    left_index: int = None
    right_index: int = None

    def is_valid(self):
        return self.left_index is not None and self.right_index is not None

    def set_side_index(self, side: Side, index: int):
        if side == Side.LEFT:
            self.left_index = index
        else:
            self.right_index = index

    def get_side_index(self, side: Side) -> int:
        if side == Side.LEFT:
            return self.left_index
        else:
            return self.right_index

    def get_opposite_side_index(self, side: Side) -> int:
        if side == Side.RIGHT:
            return self.left_index
        else:
            return self.right_index

    def shift_index(self, shift: int):
        super().shift_index(shift)
        self.left_index += shift
        self.right_index += shift

class Tree: 
    def __init__(self, chars):
        self.nodes = []

        cur_index = -1
        cur_side = Side.LEFT
        for c in chars:
            if c == '[':
                if cur_index != -1:
                    n = self.nodes[cur_index]
                    next_index = len(self.nodes)
                    n.set_side_index(cur_side, next_index)
                self.nodes.append(Branch(cur_index, cur_side))
                cur_index = len(self.nodes) - 1
                cur_side = Side.LEFT
            elif c == ',':
                cur_side = Side.RIGHT
            elif c == ']':
                n = self.nodes[cur_index]
                cur_index = n.parent_index
                cur_side = n.parent_side
            else:
                v = int(c)
                next_index = len(self.nodes)
                n = self.nodes[cur_index]
                n.set_side_index(cur_side, next_index)
                self.nodes.append(Leaf(cur_index, cur_side, v))


    def __str__(self):
        outstr = ""
        cur_index = 0
        cur_side = Side.LEFT
        cur_dir = Dir.DOWN
        while True:
            if cur_index == -1:
                break

            n = self.nodes[cur_index]
            if cur_dir == Dir.DOWN:
                if isinstance(n, Leaf):
                    outstr += str(n.value)
                    cur_dir = Dir.UP
                    cur_index = n.parent_index
                    cur_side = n.parent_side
                else:
                    if cur_side == Side.LEFT:
                        outstr += '['
                        cur_index = n.left_index
                    else:
                        outstr += ','
                        cur_index = n.right_index
                        cur_side = Side.LEFT
            else:
                if cur_side == Side.LEFT:
                    cur_side = Side.RIGHT
                    cur_dir = Dir.DOWN
                else:
                    outstr += ']'
                    cur_index = n.parent_index
                    cur_side = n.parent_side

        return outstr


    def _explode(self, index: int):
        left_index = self._find_next_value(index, Side.LEFT)
        right_index = self._find_next_value(index, Side.RIGHT)
        cur_branch = self.nodes[index]
        if left_index != -1:
            self.nodes[left_index].value += self.nodes[cur_branch.left_index].value
        if right_index != -1:
            self.nodes[right_index].value += self.nodes[cur_branch.right_index].value

        parent_index = cur_branch.parent_index
        parent_side = cur_branch.parent_side
        self.nodes[index] = Leaf(parent_index, parent_side, 0)
        

    def _find_next_value(self, start_index: int, search_side: Side) -> int:
        cur_index = start_index
        cur_dir = Dir.UP
        down_switch = False
        # print(f"find next value for index {start_index} side: {search_side}")
        while True:
            if cur_index == -1:
                break
            n = self.nodes[cur_index]
            # print(f"index: {cur_index}, {n}, state: {cur_dir}")
            if cur_dir == Dir.DOWN:
                if isinstance(n, Leaf):
                    break
                else:
                    if not down_switch:
                        cur_index = n.get_side_index(search_side)
                        down_switch = True
                    else:
                        cur_index = n.get_opposite_side_index(search_side)
            else:
                cur_index = n.parent_index
                if n.parent_side != search_side:
                    cur_dir = Dir.DOWN
        return cur_index

    def print_nodes(self):
        for i,n in enumerate(self.nodes):
            print(f"{i}: {n}")

    def maybe_explode(self) -> bool:
        cur_dir = Dir.DOWN
        cur_index = 0
        nestings = 0
        cur_side = Side.LEFT
        while True:
            if cur_index == -1:
                break
            n = self.nodes[cur_index]
            # print(f"index: {cur_index}, nestings: {nestings}, {n}, state: {cur_dir}, {cur_side}")

            if nestings == 5 and not isinstance(n, Leaf):
                # print(f"Exploding at index {cur_index}")
                self._explode(cur_index)
                return True

            if cur_dir == Dir.DOWN:
                if isinstance(n, Leaf):
                    cur_dir = Dir.UP
                    cur_index = n.parent_index
                    cur_side = n.parent_side
                else:
                    if cur_side == Side.LEFT:
                        nestings += 1
                        cur_index = n.left_index
                    else:
                        nestings += 1
                        cur_index = n.right_index
                        cur_side = Side.LEFT
            else:
                if cur_side == Side.LEFT:
                    nestings -= 1
                    cur_side = Side.RIGHT
                    cur_dir = Dir.DOWN
                else:
                    nestings -= 1
                    cur_index = n.parent_index
                    cur_side = n.parent_side
        return False

    def _split(self, index: int):
        n = self.nodes[index]
        lval = math.floor(n.value/2.0)
        rval = math.ceil(n.value/2.0)
        max_index = len(self.nodes)
        lidx = max_index
        ridx = lidx + 1
        self.nodes.append(Leaf(index, Side.LEFT, lval))
        self.nodes.append(Leaf(index, Side.RIGHT, rval))
        self.nodes[index] = Branch(n.parent_index, n.parent_side, lidx, ridx)

    def maybe_split(self) -> bool:
        cur_dir = Dir.DOWN
        cur_index = 0
        cur_side = Side.LEFT
        while True:
            if cur_index == -1:
                break
            n = self.nodes[cur_index]

            if isinstance(n, Leaf) and n.value >= 10:
                # print(f"Splitting at index {cur_index}")
                self._split(cur_index)
                return True

            if cur_dir == Dir.DOWN:
                if isinstance(n, Leaf):
                    cur_dir = Dir.UP
                    cur_index = n.parent_index
                    cur_side = n.parent_side
                else:
                    if cur_side == Side.LEFT:
                        cur_index = n.left_index
                    else:
                        cur_index = n.right_index
                        cur_side = Side.LEFT
            else:
                if cur_side == Side.LEFT:
                    cur_side = Side.RIGHT
                    cur_dir = Dir.DOWN
                else:
                    cur_index = n.parent_index
                    cur_side = n.parent_side
        return False

    def add(self, other):
        # self.print_nodes()
        # other.print_nodes()
        last_index = len(self.nodes)
        new_root = [Branch(-1, Side.LEFT, left_index=1, right_index=last_index+1)] 

        new_self = self.nodes 
        for n in new_self:
            n.shift_index(1)
        new_self[0].parent_index = 0
        new_self[0].parent_side = Side.LEFT   

        new_other = other.nodes
        for n in new_other:
            n.shift_index(last_index+1)
        new_other[0].parent_index = 0   
        new_other[0].parent_side = Side.RIGHT   

        self.nodes = new_root + new_self + new_other
        # self.print_nodes()
        self._reduce()
    
    def _reduce(self):
        while True:
            op_count = 0
            while self.maybe_explode():
                # print(self)
                op_count += 1
            if self.maybe_split():
                # print(self)
                op_count += 1
                continue
            elif op_count == 0:
                break

    def magnitude(self):
        return self._magnitude(0)

    def _magnitude(self, index):
        if isinstance(self.nodes[index], Leaf):
            return self.nodes[index].value
        else:
            lidx = self.nodes[index].left_index
            ridx = self.nodes[index].right_index
            return 3*self._magnitude(lidx) + 2*self._magnitude(ridx)

def part1():
    t = Tree(data_rows[0])
    for s in data_rows[1:]:
        t.add(Tree(s))
    print(t)
    print(t.magnitude())

# part1()

def part2():
    max_mag = 0
    for i in range(len(data_rows)):
        for j in range(len(data_rows)):
            if i == j:
                continue
            t1 = Tree(data_rows[i])
            t2 = Tree(data_rows[j])
            t1.add(t2)
            m = t1.magnitude()
            if m > max_mag:
                max_mag = m
    print(max_mag)

part2()
                    
