import sys
sys.path.append('.')
import aoc
import math
import copy

data_rows = aoc.get_input(3, sample=False).splitlines()

def bin_list_to_int(binlist: list[bool]):
    num = 0
    power = 0
    for i in range(len(binlist), 0, -1):
        num += math.pow(2, power) * binlist[i-1]
        power += 1
    return num

def gamma_rate(rows):
    n_digits = len(rows[0])
    accum = [0 for i in range(n_digits)]
    for row in rows:
        for i in range(n_digits):
            accum[i] += 1 if row[i] == '1' else -1
    g_rate_bin = [True if a > 0 else False for a in accum ]
    return g_rate_bin
    

def part1(): 
    g_rate_bin = gamma_rate(data_rows)
    print(g_rate_bin)
    g_rate = bin_list_to_int(g_rate_bin)
    print(g_rate)
    e_rate_bin = [not g for g in g_rate_bin]
    print(e_rate_bin)
    e_rate = bin_list_to_int(e_rate_bin)
    print(e_rate)
    print(g_rate * e_rate)

part1()

def digit_count(rows, index):
    count = 0
    for row in rows:
        count += 1 if row[index] == '1' else -1
    return count

def filter(rows, index, mcb):
    count = digit_count(rows, index)
    keep_val = None
    if mcb:
        keep_val = 1 if count >= 0 else 0
    else:
        keep_val = 0 if count >= 0 else 1

    new_rows = []
    for row in rows:
        if int(row[index]) == keep_val:
            new_rows.append(row)
    
    return new_rows

def part2():

    n_digits = len(data_rows[0])
    ox_rat = None
    co2_rat = None
    rows = copy.deepcopy(data_rows)
    for i in range(n_digits):
        rows = filter(rows, i, True)
        # print(rows)
        if len(rows) == 1:
            binlist = [True if i == "1" else False for i in rows[0]]
            ox_rat = bin_list_to_int(binlist)
            break
    rows = copy.deepcopy(data_rows)
    for i in range(n_digits):
        rows = filter(rows, i, False)
        # print(rows)
        if len(rows) == 1:
            binlist = [True if i == "1" else False for i in rows[0]]
            co2_rat = bin_list_to_int(binlist)
            break
    print(ox_rat*co2_rat)
    
part2()