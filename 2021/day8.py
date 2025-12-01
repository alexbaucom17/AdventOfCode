import sys
sys.path.append('.')
import aoc
import math

data_rows = aoc.get_input(8, sample=False).splitlines()

def parse():
    parsed_rows = []
    for row in data_rows:
        inputs, outputs = row.split('|')
        inputs_parsed = inputs.strip().split()
        outputs_parsed = outputs.strip().split()
        parsed_rows.append(tuple((inputs_parsed, outputs_parsed)))
    return parsed_rows

def part1():
    parsed_rows = parse()
    digit_count = 0
    for _, outputs in parsed_rows:
        for seq in outputs:
            if len(seq) in [2,3,4,7]:
                digit_count += 1
    print(digit_count)

part1()


nominal_map = {"cf": 1, "abcefg": 0, "acdeg": 2, "acdfg": 3, "bcdf": 4, "abdfg": 5, "abdefg": 6, "acf": 7, "abcdefg": 8, "abcdfg": 9}
def find_mapping(inputs):
    known_nums = {}
    mapping = {c: None for c in "abcdefg"}

    # Collect easy known numbers
    for seq in inputs:
        if len(seq) == 2:
            known_nums[1] = sorted(seq)
        if len(seq) == 3:
            known_nums[7] = sorted(seq)
        if len(seq) == 4:
            known_nums[4] = sorted(seq)
        if len(seq) == 7:
            known_nums[8] = sorted(seq)

    # Get top section
    lefts = known_nums[1]
    top = None
    for c in known_nums[7]:
        if c not in lefts:
            top = c
            break
    mapping["a"] = top

    # Find the 3
    for seq in inputs:
        if len(seq) == 5:
            is_three = True
            for c in known_nums[7]:
                if c not in seq:
                    is_three = False
                    break
            if is_three:
                known_nums[3] = sorted(seq)
                break

    # Isolate middle and bottom segment
    mid = None
    bot = None
    for c in known_nums[3]:
        if c not in known_nums[1] and c in known_nums[4]:
            mid = c
        elif c not in known_nums[7] and c not in known_nums[4]:
            bot = c
    mapping["d"] = mid
    mapping["g"] = bot

    # Isolate b segment
    for c in known_nums[4]:
        if c not in known_nums[1] and c not in mid:
            mapping["b"] = c
            break

    # Find 6
    for seq in inputs: 
        if len(seq) == 6:
            is_six = False
            for c in known_nums[1]:
                if c not in seq:
                    is_six = True
                    mapping["c"] = c
                    break
            if is_six:
                known_nums[6] = sorted(seq)
                break

    # Map last segments (e,f)
    for c in known_nums[1]:
        if c != mapping["c"]:
            mapping["f"] = c
            break

    for c in "abcdefg":
        if c not in mapping.values():
            mapping["e"] = c
            break

    return mapping

def inv_map(mapping):
    new_map = {}
    for key, val in mapping.items():
        new_map[val] = key
    return new_map

def decode(mapping, outputs):
    vals = []
    for o in outputs:
        # print(o)
        mapped_seq = []
        for c in o:
            mapped_seq.append(mapping[c])
        mapped_seq = "".join(sorted(mapped_seq))
        # print(mapped_seq)
        vals.append(nominal_map[mapped_seq])
    
    out = 0
    for i in range(4):
        out += math.pow(10, i) * vals[3-i]
    return out

def part2():
    total = 0
    for inputs, outputs in parse():
        mapping = find_mapping(inputs)
        # print(mapping)
        inv = inv_map(mapping)
        # print(inv)
        value = decode(inv, outputs)
        # print(value)
        total += value

    print(total)

part2()