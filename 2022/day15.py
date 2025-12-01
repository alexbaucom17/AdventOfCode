import sys
sys.path.append('.')
import aoc
import math
import numpy as np
import re
from operator import itemgetter
import time

data_rows = aoc.get_input(15, sample=False, index=0).splitlines()

def parse_input(rows):
  sensor_map = {}
  for row in rows:
    matches = re.findall("[-0-9]+", row)
    sensor_x = int(matches[0])
    sensor_y = int(matches[1])
    beacon_x = int(matches[2])
    beacon_y = int(matches[3])
    sensor_map[(sensor_x, sensor_y)] = (beacon_x, beacon_y)
  return sensor_map

# dist = abs(sx-bx) + abs(sy-by)
# dist - abs(sy-by) = abs(sx-bx)
# +/-(dist - abs(sy-by)) = sx-bx
# bx = sx +/- (dist - abs(sy-by))
def compute_x_coverage_range(sensor_pos, beacon_pos, y_val):
  s = np.asarray(sensor_pos, dtype=int)
  b = np.asarray(beacon_pos, dtype=int)
  dist = np.sum(np.abs(b-s))

  sensor_to_y =  np.abs(s[1] - y_val)
  # If the candidate row is further than dist, there is no coverage
  if sensor_to_y > dist:
    return None
  x1 = s[0] + (dist - sensor_to_y)
  x2 = s[0] - (dist - sensor_to_y)
  min_x = min(x1, x2)
  max_x = max(x1, x2)
  return np.asarray((min_x, max_x), dtype=int)

def merge_1d_ranges(ranges):

  if len(ranges) == 1:
    return [tuple(ranges[0])]

  # print(ranges)
  tmp_ranges = []
  id = 0
  for r in ranges:
    tmp_ranges.append((r[0], id))
    tmp_ranges.append((r[1], id))
    id += 1
  sorted_ranges = sorted(tmp_ranges, key=itemgetter(0))
  # print(sorted_ranges)

  merged_ranges = []
  open_id = set()
  min_ix = 0
  open_id.add(sorted_ranges[min_ix][1])
  max_ix = 0
  while True:
    max_ix += 1
    if max_ix >= len(sorted_ranges):
      merged_ranges.append((sorted_ranges[min_ix][0], sorted_ranges[max_ix-1][0]))
      break

    next_id = sorted_ranges[max_ix][1]
    # If id is in our set, remove it
    if next_id in open_id:
      open_id.remove(next_id)

      # If the set is empty, figure out what to do next
      if not open_id:
        next_ix = max_ix + 1

        # If set is empty and we are at the end of the list, update ranges and break
        if next_ix >= len(sorted_ranges):
          merged_ranges.append((sorted_ranges[min_ix][0], sorted_ranges[max_ix][0]))
          break
        else:
          # If set is empty but next slot has same number, add this id and continue looping
          if sorted_ranges[next_ix][0] == sorted_ranges[max_ix][0]:
            while sorted_ranges[next_ix][0] == sorted_ranges[max_ix][0]:
              next_ix += 1
              if next_ix > len(sorted_ranges):
                break
            open_id.add(sorted_ranges[next_ix-1][1])
            max_ix = next_ix
          
          # Otherwise, this is just the end of a range and we move to the next one
          else:
            merged_ranges.append((sorted_ranges[min_ix][0], sorted_ranges[max_ix][0]))
            min_ix = next_ix
            max_ix = next_ix
            open_id.add(sorted_ranges[min_ix][1])
      else:
        continue
    else:
      open_id.add(next_id)
  
  # print(merged_ranges)
  return merged_ranges

# Note - inputs are large!! Need to handle offset and sparsity
# Can't just set all intermediate points to "known" value, will need to determine point ranges that are known
# Not actually a huge number of beacons and sensors - can probably do something like figure out min/max point in given row that are covered by sensor/beacon pair
def part1():
  target_row = 2000000
  sensor_map = parse_input(data_rows)
  coverage_ranges = []
  for sensor, beacon in sensor_map.items():
    range1 = compute_x_coverage_range(sensor, beacon, target_row)
    if range1 is not None:
      coverage_ranges.append(range1)
  merged_ranges = merge_1d_ranges(coverage_ranges)
  total = 0
  for r in merged_ranges:
    total += r[1] - r[0]
  print(total)

# part1()

def part2():
 max_val = 4000000
 sensor_map = parse_input(data_rows)
 t_start = time.time()
 for i in range(max_val):

  if i % 10000 == 0:
    print(f"Iteration: {i}/{max_val}: {i/max_val*100:2f}%. Elapsed time: {time.time()-t_start}")

  coverage_ranges = []
  for sensor, beacon in sensor_map.items():
    range1 = compute_x_coverage_range(sensor, beacon, i)
    if range1 is not None:
      coverage_ranges.append(range1)
  merged_ranges = merge_1d_ranges(coverage_ranges)
  if len(merged_ranges) > 1:
    for j in range(len(merged_ranges)-1):
      min_diff = merged_ranges[j][1]
      max_diff = merged_ranges[j+1][0]
      if (max_diff - min_diff) == 2 and (min_diff + 1) > 0 and (min_diff + 1) < max_val:
        x_val = min_diff + 1
        print(f"Found at {x_val},{i}: {x_val * 4000000 + i}")

# part2()

def part2_hack():
  x = "3433501"
  y = "2908372"
  z = int(x) * 4000000 + int(y)
  print(z)

part2_hack() 