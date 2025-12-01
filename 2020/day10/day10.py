import numpy as np
from scipy.special import comb

def load_data(filename):
    with open(filename) as f:
        data = [int(line.rstrip()) for line in f]
        return data

def count_joltage_differences(data):

    data.sort()
    data = [0] + data
    data.append(data[-1]+3)
    diffs = np.diff(np.asarray(data))
    u,counts = np.unique(diffs, return_counts=True)
    print(u)
    print(counts)
    print(counts[0] * counts[1])


def count_subs(data):
    pass


def count_combos(data):
    data.sort()
    data = [0] + data
    data.append(data[-1]+3)
    diffs = np.diff(np.asarray(data))
    indexes_of_3 = np.where(diffs == 3)
    combos = 0 * (diffs == 1) + 1 * (diffs == 3)

    print(data)
    print(diffs)
    print(combos)
    print(indexes_of_3)

    count = 0
    counts_of_1 = []
    for i in diffs:
        if i == 1:
            count += 1
        else:
            counts_of_1.append(count)
            count = 0
    
    combo_map = {0: 0, 1: 0, 2: 2, 3: 4, 4:7}
    print(counts_of_1)
    combos_of_1 = []
    for n in counts_of_1:
        if n in combo_map.keys():
            combos_of_1.append(combo_map[n])
            continue
        n = n-1
        total_combos = 1
        for k in range(n):
            total_combos += comb(n, k, exact=True)
        combos_of_1.append(total_combos)
    print(combos_of_1)
    total = 1
    for n in combos_of_1:
        if n != 0:
            total*=n
    print(total)

    
    # start_idx = 0
    # end_idx = 1
    # for i in range(len(indexes_of_3)):
    #     end_idx = indexes_of_3[i]
    #     sub_counts = count_subs(data[start_idx, end_idx])



if __name__ == '__main__':

    sample_data1 = load_data("day10/sample_input1.txt")
    sample_data2 = load_data("day10/sample_input2.txt")
    data = load_data("day10/input.txt")

    #count_joltage_differences(data)
    count_combos(data)

