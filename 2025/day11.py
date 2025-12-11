
import sys
sys.path.append('.')
import aoc
from aoc_utils import parsing
import dataclasses

data_rows = aoc.get_input(day=11, sample=False, index=1).splitlines()

@dataclasses.dataclass
class Device:
  outputs: set[str]
  num_paths: int | None = None

def build_devices(data_rows) -> dict[str, Device]:
  devices: dict[str, Device] = {}
  for row in data_rows:
    s = row.split(":")
    name = s[0]
    outputs = s[1].split()
    devices[name] = Device(set(outputs))
  return devices

def find_n_paths(start: str, end: str, data_rows: list[str], ignore: set[str]) -> int:
  print(f"Finding n_paths from {start} to {end}")
  devices = build_devices(data_rows)
  if end in devices:
    del devices[end]
  
  counter = 1
  to_solve = set(devices.keys())
  solved = set()
  
  # For finding a path to out, we have to add the out node with 1 path to have a final point
  # But for other searches, we need to set out to have 0 paths so that the search can end.
  devices[end] = Device(set(), num_paths=1)
  solved.add(end)
  for name in ignore:
    devices[name] = Device(set(), num_paths=0)
    solved.add(name)

  debug = False
  def dprint(s: str):
    if debug:
      print(s)

  print(f"Num devices: {len(devices)}")
  while True:
    dprint(f"Iteration: {counter}")
    dprint(f"Solved: {solved}")
    dprint(f"To solve: {to_solve}")
    dprint(f"Devices:")
    for name in devices.keys():
      dprint(f"{name}: {devices[name]}")

    if counter > 100:
      print(f"Too many iterations")
      return 0

    if start in solved:
      n_paths = devices[start].num_paths
      print(f"Num paths: {n_paths}")
      print(f"Took {counter} iterations")
      if n_paths is None:
        raise ValueError(f"Final paths is None")
      return n_paths

    # Track which elements need to get removed from to_solve after the loop
    to_solve_update = set()

    # Loop over unsolved devices
    for name in to_solve:
      device = devices[name]
      
      # If all outputs are solved, then we can solve this device
      if device.outputs.issubset(solved):

        # Compute number of paths from this device
        total_paths = 0
        for output_name in device.outputs:
          output_paths = devices[output_name].num_paths
          if output_paths is None:
            raise ValueError(f"Num paths is non for solved output {output_name}: {devices[output_name]}")
          total_paths += output_paths

        # Update paths and tracking sets
        device.num_paths = total_paths
        solved.add(name)
        to_solve_update.add(name)

    # Update to_solve
    to_solve = to_solve.difference(to_solve_update)
    counter += 1

def part1():
  n_paths = find_n_paths('you', 'out', data_rows, ignore=set())
  print(n_paths)
  
# part1()

def part2():
  # Plan - Find n_paths  
  # svr -> fft * fft -> dac * dac -> out + 
  # svr -> dac * dac -> fft * fft -> out
  svr_fft = find_n_paths('svr', 'fft', data_rows, ignore=set(['dac', 'out']))
  fft_dac = find_n_paths('fft', 'dac', data_rows, ignore=set(['svr', 'out']))
  dac_out = find_n_paths('dac', 'out', data_rows, ignore=set(['svr', 'fft']))
  paths1 = svr_fft * fft_dac * dac_out
  svr_dac = find_n_paths('svr', 'dac', data_rows, ignore=set(['fft', 'out']))
  dac_fft = find_n_paths('dac', 'fft', data_rows, ignore=set(['svr', 'out']))
  fft_out = find_n_paths('fft', 'out', data_rows, ignore=set(['svr', 'dac']))
  paths2 = svr_dac * dac_fft * fft_out
  print(f"Total paths: {paths1} + {paths2} = {paths1+paths2}")

part2()

