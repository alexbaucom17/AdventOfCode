import sys
sys.path.append('.')
import aoc
from collections import defaultdict
import dataclasses

data_rows = aoc.get_input(5, sample=False).splitlines()

@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

def expand_points(p1, p2):
    if p1.x == p2.x:
        sgn = 1 if p2.y > p1.y else -1
        return [Point(p1.x, y) for y in range(p1.y, p2.y+sgn*1, sgn)]
    elif p1.y == p2.y:
        sgn = 1 if p2.x > p1.x else -1
        return [Point(x, p1.y) for x in range(p1.x, p2.x+sgn*1, sgn)]
    else:
        sgn_x = 1 if p2.x > p1.x else -1
        sgn_y = 1 if p2.y > p1.y else -1
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        assert abs(dx) == abs(dy)
        return [Point(p1.x + sgn_x*i, p1.y + sgn_y*i) for i in range(abs(dx) + 1)]

def part1():
    overlaps = defaultdict(int)
    for row in data_rows:
        # print(row)
        s1, s2 = row.split('->')
        x1, y1 = s1.strip().split(',')
        x2, y2 = s2.strip().split(',')
        p1 = Point(int(x1), int(y1))
        p2 = Point(int(x2), int(y2))
        for p in expand_points(p1, p2):
            # print(p)
            overlaps[p] += 1

        # print("--")

    # print(overlaps)
    num = 0
    for v in overlaps.values():
        if v > 1:
            num += 1
    print(num)

part1()

