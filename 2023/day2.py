import sys
sys.path.append('.')
import aoc
import math
import dataclasses
import re

data_rows = aoc.get_input(2, sample=False, index=0).splitlines()

@dataclasses.dataclass
class Hand:
  red: int
  blue: int
  green: int

@dataclasses.dataclass
class Game:
  id: int
  hands: list[Hand]

def parse_game(row: str) -> Game:
  str_id, str_hands = row.split(':')
  id = int(re.search("\d+", str_id)[0])
  split_hands = str_hands.split(';')
  hands = []

  def color_match(color: str, hand: str) -> int:
    match = re.search(f"(?P<num>\d+) {color}", hand)
    if match:
      return int(match.groupdict()["num"])
    else:
      return 0

  for hand in split_hands:
    red_num = color_match("red", hand)
    blue_num = color_match("blue", hand)
    green_num = color_match("green", hand)
    hands.append(Hand(red=red_num, blue=blue_num, green=green_num))
  return Game(id=id, hands=hands)

def parse_input() -> list[Game]:
  games = []
  for row in data_rows:
    games.append(parse_game(row))
  return games

def game_valid(game: Game, num_red: int, num_blue: int, num_green: int) -> bool:
  for hand in game.hands:
    if hand.red > num_red or hand.blue > num_blue or hand.green > num_green:
      return False
    
  return True

def part1():
  games = parse_input()
  total = 0
  for game in games:
    if game_valid(game, 12, 14, 13):
      total += game.id
  print(total)

# part1()

def min_cubes_power(game: Game) -> int:
  min_red = 0
  min_blue = 0
  min_green = 0
  for hand in game.hands:
    min_red = max(min_red, hand.red)
    min_blue = max(min_blue, hand.blue)
    min_green = max(min_green, hand.green)
  return min_green * min_blue * min_red

def part2():
  games = parse_input()
  total = 0
  for game in games:
    total += min_cubes_power(game)
  print(total)

part2()