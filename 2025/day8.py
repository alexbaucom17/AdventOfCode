
import sys
sys.path.append('.')
import aoc
from aoc_utils import parsing
import dataclasses
import math

sample = False
n_pairs_to_check = 1000
if sample:
  n_pairs_to_check = 10
data_rows = aoc.get_input(day=8, sample=sample, index=0).splitlines()

@dataclasses.dataclass(frozen=True)
class Point:
  x: int
  y: int
  z: int

  def dist(self, other: "Point"):
    tmp = (self.x - other.x) ** 2 +  (self.y - other.y) ** 2 + (self.z - other.z) ** 2
    return tmp
  
  def __str__(self):
    return f"[{self.x},{self.y},{self.z}]"

def build_points(data_rows):
  points = []
  for row in data_rows:
    x,y,z = map(int,row.split(","))
    points.append(Point(x,y,z))
  # print(points)
  return points

def build_pairs(points):
  pairs = []
  for i in range(len(points)-1):
    for j in range(i+1, len(points)):
      p1 = points[i]
      p2 = points[j]
      d = p1.dist(p2)
      pairs.append((d, (p1, p2)))

  sorted_pairs = sorted(pairs, key=lambda x: x[0])
  print(len(sorted_pairs))
  return sorted_pairs

def check_pair(p1: Point, p2: Point, circuits: list[set[Point]]):
  added_p1 = False
  added_p2 = False
  for c in circuits:
    if p1 in c:
      c.add(p2)
      added_p1 = True
      if added_p2:
        break
    if p2 in c:
      c.add(p1)
      added_p2 = True
      if added_p1:
        break

  if not added_p1 and not added_p2:
    circuits.append(set([p1, p2]))


def merge_all(circuits: list[set[Point] | None]):
  while True:
    update = False
    for i in range(len(circuits)-1):
      for j in range(i+1, len(circuits)):
        if circuits[i] is None or circuits[j] is None:
          continue
        if circuits[i] & circuits[j]:
          # print(f"Merged circuit from {i} and {j}")
          circuits[i] |= circuits[j]
          circuits[j] = None
          update = True
    
    circuits = [c for c in circuits if c is not None]
    if not update:
      break

def part1():
  points = build_points(data_rows)
  pairs = build_pairs(points)

  circuits = []
  for k in range(n_pairs_to_check):
    d,ps = pairs[k]
    p1, p2 = ps
    # print(f"Checking points {p1} and {p2}, distance {d}.")
    check_pair(p1, p2, circuits)
    
  merge_all(circuits)
  circuits = [c for c in circuits if c is not None]
  sorted_circuits = sorted(circuits, key=lambda x: len(x), reverse=True)

  print(f"Final circuits: {len(sorted_circuits)}")
  for i, c in enumerate(sorted_circuits[:10]):
    print(f"Circuit {i}, N points: {len(c)}")

  total = 1
  for c in sorted_circuits[:3]:
    total *= len(c)
  print(total)

# part1()

def part2():
  points = build_points(data_rows)
  pairs = build_pairs(points)
  
  all_points = set(points)
  circuits = []
  k = 0
  while True:
    if k % 10 == 0:
      print(k)
    if k >= len(pairs):
      print("overflow")
      break
    d,ps = pairs[k]
    p1, p2 = ps
    # print(f"Checking points {p1} and {p2}, distance {d}.")
    check_pair(p1, p2, circuits)
    k += 1
    merge_all(circuits)
    circuits = [c for c in circuits if c is not None]
    if k > 5 and len(circuits) == 1 and circuits[0] == all_points:
      print(k)
      print(p1)
      print(p2)
      print(p1.x * p2.x)
      break
  

part2()

