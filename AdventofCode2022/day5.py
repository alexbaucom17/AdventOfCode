import sys
sys.path.append('.')
import aoc
import math
from aoc_utils.parsing import group_by_blank_lines
from typing import NamedTuple

data_rows = aoc.get_input(5, sample=False, index=0).splitlines()

def get_stack_row(row, num_cols):
    stack_row = [None for i in range(num_cols)]
    for i in range(num_cols):
        check_n = i*4 + 1
        if check_n > len(row):
            break
        stack_row[i] = row[check_n]
    return stack_row

def parse_stacks(stacks):
    num_cols = 0
    maybe_nums = stacks[-1].strip().split()
    if maybe_nums[0] == "1":
        num_cols = int(maybe_nums[-1])
    else:
        raise ValueError("Didn't find num cols")
    print(f"Found num cols: {num_cols}")
    stack_rows = []
    for row in stacks[:-1]:
        stack_rows.append(get_stack_row(row, num_cols))
    print("stack rows")
    for row in stack_rows:
        print(row)
    cols = []
    for i in range(num_cols):
        cols.append([])
        for j in range(len(stack_rows)-1, -1, -1):
            if not stack_rows[j][i].strip():
                continue
            else:
                cols[i].append(stack_rows[j][i])
    print("Parsed cols")
    for i in range(len(cols)):
        print(f"col: {i+1} -> {cols[i]}")
    return cols

class Move(NamedTuple):
    num_crates: int
    from_col: int
    to_col: int

def parse_moves(moves):
    parsed_moves = []
    for row in moves:
        words = row.split()
        parsed_moves.append(Move(
            num_crates=int(words[1]),
            from_col=int(words[3]),
            to_col=int(words[5]),
            ))
    print("Parsed moves")
    for move in parsed_moves:
        print(move)
    return parsed_moves


def parse_input(data):
    stacks, moves = group_by_blank_lines(data)
    parsed_stacks = parse_stacks(stacks)
    parsed_moves = parse_moves(moves)
    return parsed_stacks, parsed_moves

def do_move(stacks, from_col, to_col):
    if stacks[from_col]:
        elem = stacks[from_col][-1]
        stacks[to_col].append(elem)
        stacks[from_col] = stacks[from_col][:-1]

def exectue_move_line(stacks, move):
    for _ in range(move.num_crates):
        do_move(stacks, move.from_col-1, move.to_col-1)

def part1():
    stacks, moves = parse_input(data_rows)
    for move in moves:
        exectue_move_line(stacks, move)
    print("Final stacks")
    for i in range(len(stacks)):
        print(f"col: {i+1} -> {stacks[i]}")
    s = ""
    for col in stacks:
        s += col[-1]
    print(f"Solution: {s}")

# part1()

def exectue_move_line_9001(stacks, move):
    from_col = move.from_col - 1
    to_col = move.to_col -1
    n_crates = move.num_crates
    if stacks[from_col]:
        # print(f"from col: {stacks[from_col]}")
        elems = stacks[from_col][-n_crates:]
        # print(f"elems: {elems}")
        stacks[to_col] += elems
        # print(f"to col: {stacks[to_col]}")
        stacks[from_col] = stacks[from_col][:-n_crates]
        # print(f"from col: {stacks[from_col]}")
        # print("----")

def part2():
    stacks, moves = parse_input(data_rows)
    for move in moves:
        exectue_move_line_9001(stacks, move)
    print("Final stacks")
    for i in range(len(stacks)):
        print(f"col: {i+1} -> {stacks[i]}")
    s = ""
    for col in stacks:
        s += col[-1]
    print(f"Solution: {s}")

part2()


