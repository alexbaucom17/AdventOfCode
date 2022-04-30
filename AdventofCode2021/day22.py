from lib2to3.pgen2.token import OP
from optparse import Option
import sys
sys.path.append('.')
import aoc
import math
import dataclasses
import numpy as np
from enum import Enum
from typing import Optional, Tuple

data_rows = aoc.get_input(22, sample=True, index=1).splitlines()

class IntersectionResult(Enum):
    NONE = 0,
    ABBA = 1,
    BAAB = 2,
    ABAB = 3,
    BABA = 4

class CuboidIntersectionResult(Enum):
    NONE = 0,
    PARTIAL = 1,
    FULL_A = 2,
    FULl_B = 3

class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        assert self.start <= self.end
        self.count = 1 + self.end - self.start

    def in_range(self, val: int) -> bool:
        if self.start <= val <= self.end:
            return True
        return False

    def check_overlap(self, other) -> IntersectionResult:
        other_start_in_range = self.in_range(other.start)
        other_end_in_range = self.in_range(other.end)

        if other_start_in_range and other_end_in_range:
            return IntersectionResult.ABBA
        elif other_start_in_range:
            return IntersectionResult.ABAB
        elif other_end_in_range:
            return IntersectionResult.BABA
        else:
            if other.in_range(self.start):
                return IntersectionResult.BAAB
            else:
                return IntersectionResult.NONE

    def __eq__(self, __o: object) -> bool:
        return self.start == __o.start and self.end == __o.end


def merge_ranges(A: Range, B: Range) -> Optional[Range]:
    overlap = A.check_overlap(B)
    if overlap == IntersectionResult.NONE:
        return None
    elif overlap == IntersectionResult.ABBA:
        return A
    elif overlap == IntersectionResult.BAAB:
        return B
    elif overlap == IntersectionResult.ABAB:
        return Range(A.start, B.end)
    elif overlap == IntersectionResult.BABA:
        return Range(B.start, A.end)
    else:
        raise ValueError("Impossible condition")

# TODO: Handle case where A and B have same endpoint
def unique_ranges(A: Range, B: Range) -> Optional[Tuple[Range]]:
    overlap = A.check_overlap(B)
    if overlap == IntersectionResult.NONE:
        return None
    elif overlap == IntersectionResult.ABBA:
        return (Range(A.start, B.start-1), Range(B.start, B.end), Range(B.end+1, A.end))
    elif overlap == IntersectionResult.BAAB:
        return (Range(B.start, A.start-1), Range(A.start, A.end), Range(A.end+1, B.end))
    elif overlap == IntersectionResult.ABAB:
        return (Range(A.start, B.start-1), Range(B.start, A.end), Range(A.end+1, B.end))
    elif overlap == IntersectionResult.BABA:
        return (Range(B.start, A.start-1), Range(A.start, B.end), Range(B.end+1, A.end))
    else:
        raise ValueError("Impossible condition")

def test_ranges():
    assert Range(5,10) == Range(5,10)

    assert Range(5, 10).check_overlap(Range(7,8)) == IntersectionResult.ABBA
    assert Range(5, 10).check_overlap(Range(-1,18)) == IntersectionResult.BAAB
    assert Range(5, 10).check_overlap(Range(6,18)) == IntersectionResult.ABAB
    assert Range(5, 10).check_overlap(Range(-1,8)) == IntersectionResult.BABA

    assert merge_ranges(Range(5,6), Range(7,18)) == None
    assert merge_ranges(Range(5,10), Range(7,8)) == Range(5,10)
    assert merge_ranges(Range(5,10), Range(7,18)) == Range(5,18)
    assert merge_ranges(Range(5,10), Range(-1,18)) == Range(-1,18)
    assert merge_ranges(Range(5,10), Range(-1,7)) == Range(-1, 10)
    assert merge_ranges(Range(5,10), Range(5,10)) == Range(5, 10)
    assert merge_ranges(Range(5,10), Range(5, 7)) == Range(5, 10)
    assert merge_ranges(Range(5,10), Range(7, 7)) == Range(5, 10)
    assert merge_ranges(Range(5,10), Range(7, 10)) == Range(5, 10)

    assert unique_ranges(Range(1,5), Range(7,10)) == None
    assert unique_ranges(Range(1,5), Range(4,10)) == (Range(1,3), Range(4,5), Range(6,10))
    assert unique_ranges(Range(1,5), Range(5,10)) == (Range(1,4), Range(5,5), Range(6,10))
    assert unique_ranges(Range(1,5), Range(-1,10)) == (Range(-1,0), Range(1,5), Range(6,10))
    assert unique_ranges(Range(1,5), Range(-1,3)) == (Range(-1,0), Range(1,3), Range(4,5))

test_ranges()

@dataclasses.dataclass
class Cuboid:
    state: bool = False
    xrange: Range = Range(0,0)
    yrange: Range = Range(0,0)
    zrange: Range = Range(0,0)

    def in_initial_zone(self, max_val):
        if abs(self.xrange.start) > max_val or \
           abs(self.xrange.end) > max_val or \
           abs(self.yrange.start) > max_val or \
           abs(self.yrange.end) > max_val or \
           abs(self.zrange.start) > max_val or \
           abs(self.zrange.end) > max_val:
            return False
        return True

    def count(self) -> int:
        return self.xrange.count * self.yrange.count * self.zrange.count

    def has_overlap(self, other) -> CuboidIntersectionResult:
        results = []
        results.append(self.xrange.check_overlap(other.xrange))
        results.append(self.yrange.check_overlap(other.yrange))
        results.append(self.zrange.check_overlap(other.zrange))
        if all(results = IntersectionResult.NONE):
            return CuboidIntersectionResult.NONE
        elif all(results = IntersectionResult.ABBA):
            return CuboidIntersectionResult.FULL_A
        elif all(results = IntersectionResult.BAAB):
            return CuboidIntersectionResult.FULL_B
        else:
            return CuboidIntersectionResult.PARTIAL

def split_inner_cuboid(outer: Cuboid, inner: Cuboid) -> Tuple[Cuboid]:
    xranges = unique_ranges(outer.xrange, inner.xrange)
    yranges = unique_ranges(outer.yrange, inner.yrange)
    zranges = unique_ranges(outer.zrange, inner.zrange)
    new_cuboids = []
    for x in xranges:
        for y in yranges:
            for z in zranges:
                state = outer.state
                if x == inner.xrange and y == inner.yrange and z == inner.zrange:
                    state = inner.state
                new_cuboids.append(Cuboid(state, x, y, z))
    return new_cuboids

def remove_chunk(full: Cuboid, chunk: Cuboid) -> Tuple[Cuboid]:
    xranges = unique_ranges(full.xrange, chunk.xrange)

def merge_partial_cuboids(A: Cuboid, B: Cuboid) -> Tuple[Cuboid]:
    state = A.state
    new_cuboids = []
    pass


def split_partial_cuboids(A: Cuboid, B: Cuboid) -> Tuple[Cuboid]:
    pass

# TODO: correctly handle which cuboid is being 'applied' to the other for overwriting purposes
def maybe_merge_cuboids(A: Cuboid, B: Cuboid) -> Optional[Tuple[Cuboid]]:
    result = A.has_overlap(B)
    if result == CuboidIntersectionResult.NONE:
        return None
    elif result == CuboidIntersectionResult.FULL_A:
        if A.state == B.state:
            return (A)
        else:
            return split_inner_cuboid(A, B)
    elif result == CuboidIntersectionResult.FULl_B:
        if A.state == B.state:
            return (B)
        else:
            return split_inner_cuboid(B, A)
    else:
        if A.state == B.state:
            return merge_partial_cuboids(A,B)
        else:
            return split_partial_cuboids(A,B)


            

def parse_line(line) -> Cuboid:
    onoff, coords = line.split()
    c = Cuboid(state=onoff=="on")
    for i,s in enumerate(coords.split(",")):
        nums = s.split('=')[1]
        lower = int(nums.split("..")[0])
        upper = int(nums.split("..")[1])
        if i == 0:
            c.xrange = Range(lower, upper)
        elif i == 1:
            c.yrange = Range(lower, upper)
        elif i == 2:
            c.zrange = Range(lower, upper)
        else:
            raise ValueError("Invalid")
    return c

def reboot_step(mtx, cuboid, offset):
    if not cuboid.in_initial_zone(offset):
        return mtx
    mtx[cuboid.xrange.start+offset:cuboid.xrange.end+offset+1, 
        cuboid.yrange.start+offset:cuboid.yrange.end+offset+1, 
        cuboid.zrange.start+offset:cuboid.zrange.end+offset+1] = cuboid.state
    return mtx


def part1():
    data = [parse_line(line) for line in data_rows]

    bounds = 50
    dim_size = 2*bounds+1
    mtx = np.zeros((dim_size,dim_size,dim_size), dtype=bool)
    for c in data:
        mtx = reboot_step(mtx, c, bounds)

    print(np.sum(np.sum(np.sum(mtx))))

# part1()



