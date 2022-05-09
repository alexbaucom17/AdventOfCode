import sys
sys.path.append('.')
import aoc
import math
import dataclasses
import numpy as np
from enum import Enum
from typing import Optional, Tuple
from matplotlib import pyplot as plt

data_rows = aoc.get_input(22, sample=False, index=3).splitlines()

class OverlapType(Enum):
    SELF = 0,
    APPLIED = 1,
    BOTH = 2

def validate_non_overlaping(ranges):
    if ranges is None or len(ranges) < 2:
        return
    for i in range(len(ranges)-1):
        for j in range(i+1, len(ranges)):
            r1, _ = ranges[i]
            r2, _ = ranges[j]
            assert r1.has_overlap(r2) == False

def remove_invalid_ranges(ranges):
    valid = []
    for range, ot in ranges:
        if range.start <= range.end:
            valid.append((range,ot))
    return valid
class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.count = 1 + self.end - self.start

    def __repr__(self):
        return f"[{self.start},{self.end}]"

    def in_range_inclusive(self, val: int) -> bool:
        if self.start <= val <= self.end:
            return True
        return False

    def in_range_exclusive(self, val: int) -> bool:
        if self.start < val < self.end:
            return True
        return False

    def range_fully_within(self, check) -> bool:
        return self.in_range_inclusive(check.start) and self.in_range_inclusive(self.end)

    def has_overlap(self, other) -> bool:
        return self.calculate_overlaps(other) is not None

    def calculate_overlaps(self, applied):
        applied_start_in_range = self.in_range_inclusive(applied.start)
        applied_end_in_range = self.in_range_inclusive(applied.end)

        if applied_start_in_range and applied_end_in_range:
            return remove_invalid_ranges([
                (Range(self.start, applied.start-1), OverlapType.SELF),
                (Range(applied.start, applied.end), OverlapType.BOTH),
                (Range(applied.end + 1, self.end), OverlapType.SELF)
            ])
        elif applied_start_in_range:
            return remove_invalid_ranges([
                (Range(self.start, applied.start-1), OverlapType.SELF),
                (Range(applied.start, self.end), OverlapType.BOTH),
                (Range(self.end + 1, applied.end), OverlapType.APPLIED)
            ])
        elif applied_end_in_range:
            return remove_invalid_ranges([
                (Range(applied.start, self.start-1), OverlapType.APPLIED),
                (Range(self.start, applied.end), OverlapType.BOTH),
                (Range(applied.end + 1, self.end), OverlapType.SELF)
            ])
        else:
            if applied.in_range_inclusive(self.start):
                return remove_invalid_ranges([
                    (Range(applied.start, self.start-1), OverlapType.APPLIED),
                    (Range(self.start, self.end), OverlapType.BOTH),
                    (Range(self.end + 1, applied.end), OverlapType.APPLIED)
                ])
            else:
                return None


    def __eq__(self, __o: object) -> bool:
        return self.start == __o.start and self.end == __o.end

def merge_ranges(initial: Range, applied: Range):
    overlaps = initial.calculate_overlaps(applied)
    if overlaps:
        return Range(overlaps[0][0].start, overlaps[-1][0].end)
    else:
        return None

def unique_ranges(initial: Range, applied: Range):
    ranges = initial.calculate_overlaps(applied)
    return ranges


def test_ranges():


    assert Range(5,10) == Range(5,10)

    assert merge_ranges(Range(5,6), Range(7,18)) == None
    assert merge_ranges(Range(5,10), Range(7,8)) == Range(5,10)
    assert merge_ranges(Range(5,10), Range(7,18)) == Range(5,18)
    assert merge_ranges(Range(5,10), Range(-1,18)) == Range(-1,18)
    assert merge_ranges(Range(5,10), Range(-1,7)) == Range(-1, 10)
    assert merge_ranges(Range(5,10), Range(5,10)) == Range(5, 10)
    assert merge_ranges(Range(5,10), Range(5, 7)) == Range(5, 10)
    assert merge_ranges(Range(5,10), Range(7, 7)) == Range(5, 10)
    assert merge_ranges(Range(5,10), Range(7, 10)) == Range(5, 10)
    
    def check_unique_match(actual, expected):
        print(f"Actual: {actual}")
        print(f"Expected: {expected}")
        assert len(actual) == len(expected)
        for i in range(len(actual)):
            actual_range, actual_ot = actual[i]
            expected_range, expected_ot = expected[i]
            assert actual_range == expected_range, f"{actual_range} != {expected_range}"
            assert actual_ot == expected_ot, f"{actual_ot}, != {expected_ot}"

    assert unique_ranges(Range(1,5), Range(7,10)) == None
    check_unique_match(unique_ranges(Range(1,5), Range(4,10)), ((Range(1,3), OverlapType.SELF), (Range(4,5), OverlapType.BOTH), (Range(6,10), OverlapType.APPLIED)))
    check_unique_match(unique_ranges(Range(1,5), Range(5,10)), ((Range(1,4), OverlapType.SELF), (Range(5,5), OverlapType.BOTH), (Range(6,10), OverlapType.APPLIED)))
    check_unique_match(unique_ranges(Range(1,5), Range(-1,10)), ((Range(-1,0), OverlapType.APPLIED), (Range(1,5), OverlapType.BOTH), (Range(6,10), OverlapType.APPLIED)))
    check_unique_match(unique_ranges(Range(1,5), Range(-1,3)), ((Range(-1,0), OverlapType.APPLIED), (Range(1,3), OverlapType.BOTH), (Range(4,5), OverlapType.SELF)))
    check_unique_match(unique_ranges(Range(1,5), Range(1,5)), ((Range(1,5), OverlapType.BOTH),))
    check_unique_match(unique_ranges(Range(1,5), Range(1,2)), ((Range(1,2), OverlapType.BOTH), (Range(3,5), OverlapType.SELF)))
    check_unique_match(unique_ranges(Range(1,5), Range(5,5)), ((Range(1,4), OverlapType.SELF), (Range(5,5), OverlapType.BOTH)))
    check_unique_match(unique_ranges(Range(1,5), Range(4,6)), ((Range(1,3), OverlapType.SELF), (Range(4,5), OverlapType.BOTH), (Range(6,6), OverlapType.APPLIED)))

# test_ranges()

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

    def calculate_overlaps(self, applied):
        results = []
        results.append(self.xrange.calculate_overlaps(applied.xrange))
        results.append(self.yrange.calculate_overlaps(applied.yrange))
        results.append(self.zrange.calculate_overlaps(applied.zrange))
        for r in results:
            validate_non_overlaping(r)
        return results

    def has_overlap(self, applied):
        overlaps = self.calculate_overlaps(applied)
        return None not in overlaps

    def is_fully_within(self, applied):
        return  self.xrange.range_fully_within(applied.xrange) and \
                self.yrange.range_fully_within(applied.yrange) and \
                self.zrange.range_fully_within(applied.zrange)

    def __str__(self):
        return f"[{repr(self.xrange)},{repr(self.yrange)},{repr(self.zrange)}: {self.state}]"




def print_overlaps(overlaps):
    s = "Cuboid overlaps: "
    for data in overlaps:
        if data is None:
            s += "None "
        else:
            val = data[0]
            typ = data[1]
            s += f"<{str(val)}, {typ.name}> "
    print(s)


def split_cuboids(initial: Cuboid, applied: Cuboid) -> Optional[Tuple[Cuboid]]:
    overlaps = initial.calculate_overlaps(applied)
    # print(overlaps)
    if None in overlaps:
        return None

    outputs = []
    for x_overlap in overlaps[0]:
        x_rng, x_typ = x_overlap
        if x_typ == OverlapType.SELF:
            outputs.append((Cuboid(initial.state, x_rng, initial.yrange, initial.zrange), x_typ))
        elif x_typ == OverlapType.APPLIED:
            outputs.append((Cuboid(applied.state, x_rng, applied.yrange, applied.zrange), x_typ))
        else:
            for y_overlap in overlaps[1]:
                y_rng, y_typ = y_overlap
                if y_typ == OverlapType.SELF:
                    outputs.append((Cuboid(initial.state, x_rng, y_rng, initial.zrange), y_typ))
                elif y_typ == OverlapType.APPLIED:
                    outputs.append((Cuboid(applied.state, x_rng, y_rng, applied.zrange), y_typ))
                else:
                    for z_overlap in overlaps[2]:
                        z_rng, z_typ = z_overlap
                        if z_typ == OverlapType.SELF:
                            outputs.append((Cuboid(initial.state, x_rng, y_rng, z_rng), z_typ))
                        elif y_typ == OverlapType.APPLIED:
                            outputs.append((Cuboid(applied.state, x_rng, y_rng, z_rng), z_typ))
                        else:
                            outputs.append((Cuboid(applied.state, x_rng, y_rng, z_rng), z_typ)) 
    return outputs

def test_split_cuboids():
    A = Cuboid(False, Range(-5, 5), Range(-5, 5), Range(-5, 5))

    B_no_overlap = Cuboid(False, Range(10,15), Range(10, 15), Range(10, 15))
    overlaps = split_cuboids(A, B_no_overlap)
    assert(overlaps == None)

    B_no_overlap2 = Cuboid(False, Range(0, 3), Range(10, 15), Range(10, 15))
    overlaps = split_cuboids(A, B_no_overlap2)
    assert(overlaps == None)

    B_partial_overlap = Cuboid(False, Range(0, 10), Range(0, 6), Range(-1, 4))
    overlaps = split_cuboids(A, B_partial_overlap)
    assert(len(overlaps) == 7)
    print_overlaps(overlaps)

    B_full_overlap = Cuboid(False, Range(-5, 5), Range(-3, 3), Range(1, 1))
    overlaps = split_cuboids(A, B_full_overlap)
    assert(len(overlaps) == 5)
    print_overlaps(overlaps)


# test_split_cuboids() 


def apply_cuboid(initial: Cuboid, applied: Cuboid) -> Optional[Tuple[Tuple[Cuboid], Tuple[OverlapType]]]:
    splits = split_cuboids(initial, applied)
    if splits is None:
        return None

    if initial.state == applied.state:
        rtn = []
        overlap_types = []
        for c, ot in splits:
            c.state = initial.state
            rtn.append(c)
            overlap_types.append(ot)
        return rtn, overlap_types
    else:
        rtn = []
        overlap_types = []
        for c, ot in splits:
            if ot == OverlapType.SELF:
                c.state = initial.state
            else:
                c.state = applied.state
            rtn.append(c)
            overlap_types.append(ot)
        return rtn, overlap_types
            

def test_apply_cubiod():
    A = Cuboid(False, Range(-5, 5), Range(-5, 5), Range(-5, 5))

    def print_cuboids(cuboids):
        print()
        for ix, c in enumerate(cuboids[0]):
            ot = cuboids[1][ix]
            print(f"{c}, {ot}")

    B_partial_overlap_match = Cuboid(False, Range(0, 10), Range(0, 6), Range(-1, 4))
    cuboids = apply_cuboid(A, B_partial_overlap_match)
    print_cuboids(cuboids)

    B_partial_overlap_mismatch = Cuboid(True, Range(0, 10), Range(0, 6), Range(-1, 4))
    cuboids = apply_cuboid(A, B_partial_overlap_mismatch)
    print_cuboids(cuboids)

    B_full_overlap_mismatch = Cuboid(True, Range(-5, 5), Range(-5, 5), Range(-5, 5))
    cuboids = apply_cuboid(A, B_full_overlap_mismatch)
    print_cuboids(cuboids)

    B_extra_overlap_mismatch = Cuboid(True, Range(-10, 10), Range(-10, 10), Range(-10, 10))
    cuboids = apply_cuboid(A, B_extra_overlap_mismatch)
    print_cuboids(cuboids)
# test_apply_cubiod()

def check_for_duplicates(cuboids, strict=False):
    for i in range(len(cuboids)-1):
        for j in range(i+1, len(cuboids)):
            c1 = cuboids[i]
            c2 = cuboids[j]
            if c1.has_overlap(c2):
                print(f"Found overlap between {c1} and {c2}")
                if strict:
                    raise ValueError("overlap")
                


def apply_cuboid_to_set(all_cuboids: list[Cuboid], applied: Cuboid) -> list[Cuboid]:

    idx_with_overlap = []
    idx_no_overlap = []
    for idx, c in enumerate(all_cuboids):
        if c.has_overlap(applied):
            idx_with_overlap.append(idx)
        else:
            idx_no_overlap.append(idx)
    out_cuboids = [all_cuboids[i] for i in idx_no_overlap]
    print(f"Overlaps: {len(idx_with_overlap)}, Nonoverlaps: {len(idx_no_overlap)}")
    # check_for_duplicates(out_cuboids, strict=True)

    for count, idx in enumerate(idx_with_overlap):
        if count % 10 == 0:
            print(f"Performing merge {count}/{len(idx_with_overlap)}")
        c = all_cuboids[idx]

        result = apply_cuboid(c, applied)
        if result is None:
            out_cuboids.append(c)
            continue
        new_cuboids, overlap_types = result
        for idx, nc in enumerate(new_cuboids):
            overlap_type = overlap_types[idx]
            if overlap_type == OverlapType.SELF:
                out_cuboids.append(nc)
    out_cuboids.append(applied)
    return out_cuboids

            
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


def draw_mtx(mtx, name):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    print('rendering voxels...')
    ax.voxels(mtx)
    print('voxels rendered')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    for ii in range(0,360,60):
        ax.view_init(elev=0., azim=ii)
        plt.savefig(f"{name}_movie{ii}.png")
    # plt.show()

def draw_cuboids(cuboids):
    bounds = 50
    dim_size = 2*bounds+1
    mtx = np.zeros((dim_size,dim_size,dim_size), dtype=bool)
    for c in cuboids:
        mtx = reboot_step(mtx, c, bounds)
    draw_mtx(mtx, 'cuboid')

n_steps = 200000

def part1():
    data = [parse_line(line) for line in data_rows]

    bounds = 50
    dim_size = 2*bounds+1
    mtx = np.zeros((dim_size,dim_size,dim_size), dtype=bool)
    count = 0
    for c in data:
        mtx = reboot_step(mtx, c, bounds)
        count += 1
        if count > n_steps:
            break

    print(np.sum(np.sum(np.sum(mtx))))
    # draw_mtx(mtx, 'mtx')

# part1()


def part1_sparse():
    data = [parse_line(line) for line in data_rows]
    cuboid_set = []
    count = 0
    for c in data:
        print(f"Applying {c}")
        # if not c.in_initial_zone(50):
        #     continue
        cuboid_set = apply_cuboid_to_set(cuboid_set, c)
        # check_for_duplicates(cuboid_set, strict=True)
        # for c in cuboid_set:
        #     print(c)
        print()
        count += 1
        if count > n_steps:
            break
    total = 0
    for c in cuboid_set:
        if c.state:
            total += c.count()
    print(total)
    # check_for_duplicates(cuboid_set)
    # draw_cuboids(cuboid_set)
part1_sparse()





