import sys
sys.path.append('.')
import aoc
import math
import numpy as np

data_rows = aoc.get_input(10, sample=False, index=0).splitlines()

class CPU:

  def __init__(self, instructions):
    self.instructions = instructions
    self.x = 1
    self.cycle = 1
    self.instruction_count = 0
    self.in_addx = False
    self.arr = np.zeros((240,1), dtype=bool)

  def step(self):
    if self.cycle < 240:
      pos = self.cycle-1
      mod_pos = pos % 40
      check_array = np.asarray([self.x-1, self.x, self.x+1])
      val = np.any(mod_pos == check_array).astype(bool)
      self.arr[pos] = val
    
    if self.in_addx:
      v = self.instructions[self.instruction_count].split()[1]
      self.x += int(v)
      self.in_addx = False
      self.instruction_count += 1
    else:
      op = self.instructions[self.instruction_count].split()[0]
      if op == "noop":
        self.instruction_count += 1
      elif op == "addx":
        self.in_addx = True
      else:
        raise ValueError("Unknown operation")
    self.cycle += 1  

  def done(self):
    return self.instruction_count >= len(self.instructions)

  def signal_strength(self):
    return self.x*self.cycle  

    

def part1():
  cpu = CPU(data_rows)
  checks = [20, 60, 100, 140, 180, 220]
  strengths = []

  while (not cpu.done()):
    cpu.step()
    if cpu.cycle in checks:
      strengths.append(cpu.signal_strength())

  print(strengths)
  print(sum(strengths))

# part1()

def part2():
  cpu = CPU(data_rows)
  while (not cpu.done()):
    cpu.step()
  arr = cpu.arr.reshape((6,40))
  for i in range(6):
    s = ""
    for v in arr[i,:]:
      s += "#" if v else "."
    print(s)


part2()