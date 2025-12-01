import sys
sys.path.append('.')
import aoc
import math
from collections import defaultdict

data_rows = aoc.get_input(14, sample=False).splitlines()

def chain_step(chain, rules):
    new_chain = ""
    for i in range(len(chain) - 1):
        pair = chain[i:i+2]
        new_val = rules[pair]
        new_chain += pair[0] + new_val

    new_chain += chain[-1]
    return new_chain

def score_chain(chain):
    letters = defaultdict(int)
    for c in chain:
        letters[c] += 1
    values = letters.values()
    low = min(values)
    high = max(values)
    return high - low

def better_chain_step(pairs, rules):
    new_pairs = defaultdict(int)
    for pair, num in pairs.items():
        new_char = rules[pair]
        new_pair1 = pair[0] + new_char
        new_pair2 = new_char + pair[1]
        # print(f"From {pair}:{num} generates char: {new_char} -> {new_pair1} and {new_pair2}")
        new_pairs[new_pair1] += num
        new_pairs[new_pair2] += num
        # print(new_pairs)
    return new_pairs

def parse():
    start_chain = data_rows[0]
    rules = {}
    for row in data_rows[2:]:
        base, new = row.split('->')
        rules[base.strip()] = new.strip()

    pairs = defaultdict(int)
    for i in range(len(start_chain) - 1):
        pair = start_chain[i:i+2]
        pairs[pair] += 1

    return (pairs, rules, start_chain[-1])

def better_chain_score(pairs, last_letter):
    letter_counts = defaultdict(int)
    for pair, count in pairs.items():
        letter_counts[pair[0]] += count
    letter_counts[last_letter] += 1
    values = letter_counts.values()
    low = min(values)
    high = max(values)
    return high - low

def part1():
    pairs, rules, last_letter = parse()
    for i in range(40):
        pairs = better_chain_step(pairs, rules)
        chain_length = sum(pairs.values()) + 1
        print(f"step: {i}, length: {chain_length}")
        # print(pairs)
    print("------")
    print(better_chain_score(pairs, last_letter))

part1()