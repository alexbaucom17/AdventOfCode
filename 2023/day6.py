import sys
sys.path.append('.')
import aoc
import math
import dataclasses

data_rows = aoc.get_input(6, sample=False, index=0).splitlines()

@dataclasses.dataclass
class Races:
  time: list[int]
  distance: list[int]

def parse_inputs() -> Races:
  times_str = data_rows[0].split()
  distance_str = data_rows[1].split()
  return Races([int(x) for x in times_str[1:]], [int(x) for x in distance_str[1:]])

def parse_inputs2() -> list[int, int]:
  times_str = data_rows[0].split()
  distance_str = data_rows[1].split()
  times_num = "".join(times_str[1:])
  distance_num = "".join(distance_str[1:])
  return int(times_num), int(distance_num)

def distance(hold_time: int, total_time: int) -> int:
  return hold_time * (total_time - hold_time)

def race_wins(win_distance: int, total_time: int) -> int:
  num_wins = 0
  for hold_time in range(total_time):
    if hold_time % 100000 == 0:
      print(f"{hold_time}/{total_time}")
    if distance(hold_time, total_time) > win_distance:
      num_wins += 1
  return num_wins


def part1():
  races = parse_inputs()
  wins = 1
  for i in range(len(races.time)):
    num_wins = race_wins(races.distance[i], races.time[i])
    print(f"Race {i} num_wins: {num_wins}")
    wins *= num_wins
  print(wins)

# part1()

def part2():
  total_time, win_distance = parse_inputs2()
  print(race_wins(win_distance, total_time))

part2()