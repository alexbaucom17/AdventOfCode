from math import gcd
import numpy as np

def load_data(filename):
    with open(filename) as f:
        data = [line.rstrip() for line in f]
        timestamp = int(data[0])
        buses = [c for c in data[1].split(',')]
        return timestamp, buses

def condense_buses(buses):
    return [int(b) for b in buses if b != 'x']

def any_bus_arrives(time, buses):
    for b in buses:
        if time % b == 0:
            return b
    return None

def find_next_bus(timestamp, buses):
    buses = condense_buses(buses)
    count = 1
    while True:
        check_time = timestamp + count
        print("Checking time: {}".format(check_time))
        b = any_bus_arrives(check_time, buses)
        if b is not None:
            print("Found bus: {} after {} minues. Answer: {}".format(b, count, b*count))
            return
        count += 1

def calc_lcm(nums):
    lcm = nums[0]
    for i in nums[1:]:
        lcm = lcm*i//gcd(lcm, i)
    return lcm

def preprocess_bus_table(buses):
    
    # Build sets of buses
    common_table = [set() for i in buses]
    for i,b in enumerate(buses):
        if b == 'x':
            continue
        b = int(b)
        for j in range(i, len(buses), b):
            common_table[j].add(b)

    print("Common table: {}".format(common_table))

    # Find least common multiple of each set
    lcms = []
    for s in common_table:
        l = list(s)
        lcm = 0
        if len(l) >= 1:
            lcm = calc_lcm(l)
        lcms.append(lcm)
    print("lcms: {}".format(lcms))

    # Build simplified problem set
    sorted_idx = np.argsort(lcms)
    print(sorted_idx)
    problem = []
    for idx in reversed(sorted_idx):
        val = lcms[idx]
        if val != 0:
            offset = idx
            buses = common_table[idx]
            insert = True
            for _,_,b in problem:
                if buses.issubset(b):
                    insert = False
                    break
            if insert:
                problem.append((val, offset, buses))
    print("Problem: {}".format(problem))
    return problem

def solve_bus_problem(problem):
    step_size = problem[0][0]
    step_offset = problem[0][1]

    cur_mul = 0
    while True:
        cur_mul += 1
        cur_value = cur_mul * step_size - step_offset
        ok = True
        #print("Checking: {}".format(cur_value))
        for v,o,_ in problem[1:]:
            if (cur_value + o) % v != 0:
                ok = False
                break
        if ok:
            print("Found: {}".format(cur_value))
            return

        if cur_mul % 100000 == 0:
            print("Current value: {}".format(cur_value))



if __name__ == '__main__':

    sample_data = load_data("day13/sample_input.txt")
    data = load_data("day13/input.txt") 

    #find_next_bus(data[0], data[1])
    
    sample_data2 = []
    with open(("day13/sample_input2.txt")) as f:
        sample_data2 = [[c for c in line.rstrip().split(',') ] for line in f]

    problem = preprocess_bus_table(data[1])
    solve_bus_problem(problem)