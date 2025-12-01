import sys
sys.path.append('.')
import aoc

data_rows = aoc.get_input(1, sample=False).splitlines()

def part1(): 
    increased = 0
    prev = 999999999
    for row in data_rows:
        num = int(row)
        if num > prev:
            increased += 1
        prev = num

    print(increased)

part1()

def part2():
    increased = 0
    prev = 999999999
    for i in range(len(data_rows) - 2):
        nums = [int(data_rows[i+j]) for j in range(3)]
        num = sum(nums)
        if num > prev:
            increased += 1
        prev = num

    print(increased)

part2()

