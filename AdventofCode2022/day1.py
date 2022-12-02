import sys
sys.path.append('.')
import aoc
import math
from aoc_utils.parsing import group_by_blank_lines

data_rows = aoc.get_input(1, sample=True, index=0).splitlines()

def part1():
    cur_cals = 0
    max_cals = 0
    for row in data_rows:
        if not row.strip():
            if cur_cals > max_cals:
                max_cals = cur_cals
            cur_cals = 0
        else:
            cur_cals += int(row)
    print(max_cals)

# part1()

def part2():
    cals = []
    cur_cals = 0
    for row in data_rows:
        if not row.strip():
            cals.append(cur_cals)
            cur_cals = 0
        else:
            cur_cals += int(row)
    cals.append(cur_cals)

    max_3 = sorted(cals)[-3:]
    print(max_3)
    print(sum(max_3))
# part2()

def part1_test_util():
    groups = group_by_blank_lines(data_rows)
    sums = list(map(lambda row: sum([int(x) for x in row]), groups))
    print(groups)
    print(sums)
part1_test_util()