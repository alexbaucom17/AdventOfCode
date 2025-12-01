import sys
sys.path.append('.')
import aoc
import math
import numpy as np
import queue

data_rows = aoc.get_input(18, sample=False, index=0).splitlines()

def parse_inputs(rows):
  arr = np.zeros((3, len(rows)), dtype=int)
  for i,row in enumerate(rows):
    x,y,z = row.split(",")
    arr[0, i] = int(x)
    arr[1, i] = int(y)
    arr[2, i] = int(z)
  return arr

def part1():
  data = parse_inputs(data_rows)
  total = 0
  for i in range(data.shape[1]):
    diffs = data - np.broadcast_to(data[:, i].reshape((3,1)), (3, data.shape[1]))
    cube_faces = np.sum(np.abs(diffs), axis=0)
    total += np.sum(cube_faces == 1)
  all_faces = 6 * data.shape[1]
  print(all_faces-total)   

# part1()

def get_neighbors(point):
  steps = [
    [1,0,0],
    [-1,0,0],
    [0,1,0],
    [0,-1,0],
    [0,0,1],
    [0,0,-1]
  ]
  points = []
  for s in steps:
    points.append(point + np.asarray(s))
  return points

def out_of_bounds(point, min_lims, max_lims):
  above_max = np.any(point > max_lims)
  below_min = np.any(point < min_lims)
  return above_max or below_min

def part2():
  explored = set()
  np_rocks = parse_inputs(data_rows)
  min_lims = np.min(np_rocks, axis=1)
  max_lims = np.max(np_rocks, axis=1)
  min_lims -= 1
  max_lims += 1
  rock = set([tuple(np_rocks[:,i]) for i in range(np_rocks.shape[1])])
  # print(rock)
  q = queue.Queue()
  q.put(max_lims)
  surface_area = 0

  print(min_lims)
  print(max_lims)

  while not q.empty():

    point = q.get()
    # print("-------------")
    # print(point)

    for n in get_neighbors(point):
      # print(n)
      if out_of_bounds(n, min_lims, max_lims):
        # print("oob")
        continue
      if tuple(n) in explored:
        # print("explored")
        continue
      if tuple(n) in rock:
        # print("rock")
        surface_area += 1
        continue

      # print("queued")
      q.put(n)
      explored.add(tuple(n))

  print(len(explored))
  print(surface_area)

part2()