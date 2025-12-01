import sys
sys.path.append('.')
import aoc
import math
from aoc_utils.parsing import group_by_blank_lines
import re

data_rows = aoc.get_input(11, sample=False, index=0).splitlines()

class Monkey:
  def __init__(self, id, starting_items, operation, test, true_id, false_id, skip_div):
    self.id = id
    self.items = starting_items
    self.op = operation
    self.test = test
    self.true_id = true_id
    self.false_id = false_id
    self.num_checks = 0
    self.skip_div = skip_div
    self.modulator = 1

  def turn(self):
    moves = []
    for item in self.items:
      self.num_checks += 1
      item = self.op(item)
      if self.skip_div:
        item = item % self.modulator
      else:
        item = math.floor(item/3)
      if self.test(item):
        moves.append((self.true_id, item))
      else:
        moves.append((self.false_id, item))
    self.items = []
    return moves

  def catch_item(self, item):
    self.items.append(item)

  def set_modulator(self, modulator):
    self.modulator = modulator

def parse_monkey(text, skip_div):
  monkey_id = int(re.search("[0-9]+", text[0])[0])
  # print(monkey_id)

  starting_items = re.findall("[0-9]{2}", text[1])
  starting_items = [int(n) for n in starting_items]
  # print(starting_items)

  op_line = text[2]
  if op_line.find("old * old") != -1:
    # print("old*old")
    op = lambda x: x*x
  elif op_line.find("old * ") != -1:
    # print("old*")
    n = int(op_line.split("*")[1].strip())
    op = lambda x: x*n
  elif op_line.find("old + ") != -1:
    # print("old+")
    n = int(op_line.split("+")[1].strip())
    op = lambda x: x+n
  else:
    raise ValueError(f"Couldn't find op in {op_line}")

  divisor_num = int(re.search("[0-9]+", text[3])[0])
  test = lambda x: x % divisor_num == 0

  true_id = int(re.search("[0-9]+", text[4])[0])
  false_id = int(re.search("[0-9]+", text[5])[0])

  return Monkey(monkey_id, starting_items, op, test, true_id, false_id, skip_div), divisor_num

def part1():
  text_blocks = group_by_blank_lines(data_rows)
  monkeys = []
  for text in text_blocks:
    m, _ = parse_monkey(text, False)
    monkeys.append(m)

  for i in range(20):
    for m in monkeys:
      moves = m.turn()
      for id, item in moves:
        monkeys[id].catch_item(item)
  
  checks = []
  for m in monkeys:
    checks.append(m.num_checks)
  # print(checks)
  sorted_checks = sorted(checks, reverse=True)
  print(sorted_checks[0] * sorted_checks[1])  

# part1()

def part2():
  text_blocks = group_by_blank_lines(data_rows)
  monkeys = []
  total_div = 1
  for text in text_blocks:
    m, divisor = parse_monkey(text, True)
    monkeys.append(m)
    total_div *= divisor
  for m in monkeys:
    m.set_modulator(total_div)

  for i in range(10000):
    for m in monkeys:
      moves = m.turn()
      for id, item in moves:
        monkeys[id].catch_item(item)
  
  checks = []
  for m in monkeys:
    checks.append(m.num_checks)
  print(checks)
  sorted_checks = sorted(checks, reverse=True)
  print(sorted_checks[0] * sorted_checks[1])  

part2()