import sys
sys.path.append('.')
import aoc
import math

data_rows = aoc.get_input(10, sample=False).splitlines()

class Node:
    def __init__(self, open, parent_index):
        self.open = open
        self.close = None
        self.parent_index = parent_index

open_chars = "([{<"
close_chars = ")]}>"
char_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
char_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
char_ac_scores = {")": 1, "]": 2, "}": 3, ">": 4}

class Tree:
    def __init__(self):
        self.nodes = []
        self.cur_index = None

    def add_char(self, char):
        if char in open_chars:
            self._add_node(char)
            return None
        else:
            return self._close_node(char)

    def _add_node(self, char):
        self.nodes.append(Node(char, self.cur_index))
        self.cur_index = len(self.nodes) - 1

    def _close_node(self, char):
        cur_node = self.nodes[self.cur_index]
        if char_pairs[cur_node.open] == char:
            cur_node.close = char
            self.cur_index = cur_node.parent_index
        else:
            return char

    def autocomplete(self):
        ac_seq = []
        while self.cur_index is not None:
            cur_node = self.nodes[self.cur_index]
            ac_seq.append(char_pairs[cur_node.open])
            self.cur_index = cur_node.parent_index
        return ac_seq

def parse_row_and_score(row):
    tree = Tree()
    for char in row:
        rtn = tree.add_char(char)
        if rtn:
            return char_scores[rtn]
    return 0

def part1():
    total = 0
    for row in data_rows:
        total += parse_row_and_score(row)
    print(total)
part1()

def score_ac(ac_seq):
    total = 0
    for char in ac_seq:
        total *= 5
        total += char_ac_scores[char]
    return total

def parse_row_and_score_incomplete(row):
    tree = Tree()
    for char in row:
        rtn = tree.add_char(char)
        if rtn:
            return 0
    ac_seq = tree.autocomplete()
    return score_ac(ac_seq)

def part2():
    scores = []
    for row in data_rows:
        score = parse_row_and_score_incomplete(row)
        if score != 0:
            scores.append(score)

    sorted_scores = sorted(scores)
    idx = math.floor(len(scores)/2)
    print(sorted_scores[idx])
part2()