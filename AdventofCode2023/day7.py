import sys
sys.path.append('.')
import aoc
import math
from enum import IntEnum
from collections import Counter

data_rows = aoc.get_input(7, sample=False, index=0).splitlines()

card_chars = "0123456789TJQKA"
card_chars_joker = "0J23456789TXQKA"

class HandType(IntEnum):
  High = 0
  Pair = 1
  Two_Pair = 2
  Three = 3
  Full = 4
  Four = 5
  Five = 6

def classify_hand(hand_ints: list[int], use_joker: bool) -> HandType:
  element_counts = Counter(hand_ints)
  num_jokers = 0
  if use_joker:
    num_jokers = element_counts[card_chars_joker.index("J")]
    if num_jokers == 5:
      return HandType.Five
    del element_counts[card_chars_joker.index("J")]

  sorted_counts = sorted(element_counts.values())
  sorted_counts[-1] += num_jokers

  if sorted_counts == [5]:
    return HandType.Five
  elif sorted_counts == [1,4]:
    return HandType.Four
  elif sorted_counts == [2,3]:
    return HandType.Full
  elif sorted_counts == [1,1,3]:
    return HandType.Three
  elif sorted_counts == [1,2,2]:
    return HandType.Two_Pair
  elif sorted_counts == [1,1,1,2]:
    return HandType.Pair
  elif sorted_counts == [1,1,1,1,1]:
    return HandType.High
  else:
    raise ValueError(f"Invalid sorted_counts: {sorted_counts}")
  

def build_hand(hand_str: str, use_joker: bool) -> tuple[int]:
  hand_ints = []
  for char in hand_str:
    if use_joker:
      hand_ints.append(card_chars_joker.index(char))
    else:
      hand_ints.append(card_chars.index(char))
      
  hand_type = classify_hand(hand_ints, use_joker)
  return tuple([int(hand_type)] + hand_ints)

def parse_inputs(use_joker: bool):
  hands = []
  for row in data_rows:
    hand, bid = row.split()
    hand_tuple = build_hand(hand, use_joker)
    hands.append((hand_tuple, int(bid)))
  return hands

def hand_tuple_str(hand_tuple: tuple[int], use_joker: bool) -> str:
  hand_type = HandType(hand_tuple[0])
  if use_joker:
    hand_chars = "".join([card_chars_joker[i] for i in hand_tuple[1:]])
  else:
    hand_chars = "".join([card_chars[i] for i in hand_tuple[1:]])
  return f"Hand {hand_chars} is of type: {hand_type.name}, raw: {hand_tuple}"

def part1():
  hands = parse_inputs(use_joker=False)
  sorted_hands = sorted(hands, key=lambda x: x[0])
  total = 0
  for rank, hand in enumerate(sorted_hands):
    print(f"rank: {rank+1}, bid: {hand[1]} {hand_tuple_str(hand[0], use_joker=False)}")
    total += (rank+1) * hand[1]
  print(total)

# part1()


def part2():
  hands = parse_inputs(use_joker=True)
  sorted_hands = sorted(hands, key=lambda x: x[0])
  total = 0
  for rank, hand in enumerate(sorted_hands):
    print(f"rank: {rank+1}, bid: {hand[1]} {hand_tuple_str(hand[0], use_joker=True)}")
    total += (rank+1) * hand[1]
  print(total)

part2()