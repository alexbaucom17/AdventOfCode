import sys
sys.path.append('.')
import aoc
import math

data_rows = aoc.get_input(3, sample=False, index=0).splitlines()

def part1():
    total = 0
    for row in data_rows:
        split = int(len(row.strip())/2)
        sack1 = set(row[:split])
        sack2 = set(row[split:])
        common = sack1.intersection(sack2)
        letter = common.pop()   
        score = 0
        if letter.isupper():
            score += 26
        score += ord(letter.lower()) - ord('a') + 1
        # print(f"common: {letter}, score: {score}")
        total += score
    print(total)
# part1()

def part2():
    total = 0
    for i in range(0, len(data_rows), 3):
        sack1 = set(data_rows[i].strip())
        sack2 = set(data_rows[i+1].strip())
        sack3 = set(data_rows[i+2].strip())
        common = sack1.intersection(sack2.intersection(sack3))
        letter = common.pop()   
        score = 0
        if letter.isupper():
            score += 26
        score += ord(letter.lower()) - ord('a') + 1
        # print(f"common: {letter}, score: {score}")
        total += score
    print(total)
part2()
