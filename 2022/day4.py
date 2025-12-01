import sys
sys.path.append('.')
import aoc
import math

data_rows = aoc.get_input(4, sample=False, index=0).splitlines()

def part1():
    num_overlaps = 0
    for row in data_rows:
        s1,s2 = row.strip().split(",")
        s1n1,s1n2 = s1.split("-")
        s2n1,s2n2 = s2.split("-")
        # print(f"{s1n1},{s1n2},{s2n1},{s2n2}")
        if (int(s1n1) >= int(s2n1) and int(s1n2) <= int(s2n2)) or (int(s1n1) <= int(s2n1) and int(s1n2) >= int(s2n2)):
            num_overlaps += 1
            # print("overlap")
    print(num_overlaps)   
part1()

def part1a():
    print("")
    num_overlaps = 0
    num_overlaps2 = 0
    for row in data_rows:
        s1,s2 = row.strip().split(",")
        s1n1,s1n2 = s1.split("-")
        s2n1,s2n2 = s2.split("-")
        s1_set = set([n for n in range(int(s1n1), int(s1n2)+1)])
        s2_set = set([n for n in range(int(s2n1), int(s2n2)+1)])
        common = s1_set.intersection(s2_set)
        # print(f"{s1n1},{s1n2},{s2n1},{s2n2}")
        if common == s1_set or common == s2_set:
            num_overlaps += 1
            # print("overlap")
        if len(common) > 0:
            num_overlaps2 += 1
    print(num_overlaps)
    print(num_overlaps2)
part1a()
