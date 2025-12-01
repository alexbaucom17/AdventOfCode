import sys
sys.path.append('.')
import aoc
import math

data_rows = aoc.get_input(1, sample=False, index=2).splitlines()

digits = "0123456789"

def first_digit(row):
  for c in row:
    if c in digits:
      return c
    
def last_digit(row):
  return first_digit(reversed(row))

def part1():
  print(sum([int(first_digit(row) + last_digit(row)) for row in data_rows]))

# part1()

def replace(row):
  m = {"one": "one1one", "two": "two2two", "three": "three3three", "four": "four4four", "five":"five5five",
       "zero":"zero0zero", "six": "six6six", "seven":"seven7seven", "eight":"eight8eight", "nine":"nine9nine"}
  for key, val in m.items():
    row = row.replace(key, val)
  return row

def part2():
 print(sum([int(first_digit(replace(row)) + last_digit(replace(row))) for row in data_rows]))

part2()