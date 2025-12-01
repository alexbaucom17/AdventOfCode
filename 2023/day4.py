import sys
sys.path.append('.')
import aoc
import math
from aoc_utils import parsing
import dataclasses

data_rows = aoc.get_input(4, sample=False, index=0).splitlines()

@dataclasses.dataclass
class Card:
  winning: set[int]
  have: set[int]

def parse_inputs() -> list[Card]:
  all_cards = []
  for row in data_rows:
    data = row.split(":")[1]
    cards = data.split("|")
    winning = parsing.get_numbers_with_separator(cards[0])
    have = parsing.get_numbers_with_separator(cards[1])
    all_cards.append(Card(winning=set(winning), have=set(have)))
  return all_cards

def score_card(card: Card) -> int:
  matches = card.winning & card.have
  if matches:
    return int(math.pow(2, len(matches)-1))
  else:
    return 0

def part1():
  total = 0
  for card in parse_inputs():
    total += score_card(card)
  print(total)
  

# part1()

def part2():
  cards = parse_inputs()
  card_map = {i: 1 for i in range(len(cards))}

  for i, card in enumerate(cards):
    num_matches = len(card.winning & card.have)
    if num_matches > 0:
      num_cards = card_map[i]
      for j in range(i, i+num_matches):
        card_map[j+1] += num_cards

  print(sum(card_map.values()))


part2()