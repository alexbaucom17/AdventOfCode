import sys
sys.path.append('.')
import aoc
import math
import dataclasses
from aoc_utils import parsing
from typing import Optional

data_rows = aoc.get_input(5, sample=False, index=0).splitlines()

@dataclasses.dataclass
class Range:
  dest_start: Optional[int]
  source_start: int
  num: int

  def contains_source(self, value: int) -> bool:
    return self.source_start <= value < self.source_end()
  
  def source_end(self):
    return self.source_start + self.num
  
  def source_end_value(self):
    return self.source_end() - 1
  
  def dest_end(self):
    return self.dest_start + self.num
  
  def source_to_dest_offset(self):
    return self.dest_start - self.source_start
  
  def get_dest(self, source_in):
    return source_in + self.source_to_dest_offset()

@dataclasses.dataclass()
class Quantity:
  value: int
  category: str

@dataclasses.dataclass
class ParsedMapping:
  source: str
  dest: str
  ranges: list[list[int]]

def parse_inputs() -> list[list[Quantity], list[ParsedMapping]]:
  groups = parsing.group_by_blank_lines(data_rows)

  seeds = parsing.get_numbers_with_separator(str(groups[0][0][6:]))
  seed_quantities = [Quantity(value, "seed") for value in seeds]

  mappings = []
  for group in groups[1:]:
    source, _, dest = group[0].split()[0].split('-')
    ranges = [Range(*parsing.get_numbers_with_separator(row)) for row in group[1:]]
    mappings.append(ParsedMapping(source, dest, ranges))

  return seed_quantities, mappings


class RangeMap:

  def __init__(self, source: str, destination: str, ranges: list[Range]):
    self.source = source
    self.destination = destination
    self.ranges = sorted(ranges, key=lambda x: x.source_start)

  def lookup(self, source: Quantity) -> Quantity:
    if source.category != self.source:
      raise ValueError(f"Incorrect category {source.category} for map {self.source} to {self.destination}")
    
    for range in self.ranges:
      if range.contains_source(source.value):
        return Quantity(range.get_dest(source.value), self.destination)
      
    return Quantity(source.value, self.destination)
  
  def lookup_ranges(self, ranges_in: list[Range]) -> list[Range]:
    # print("lookup ranges")
    ranges_out = []
    for r in ranges_in:
      ranges_out += self._lookup_range(r)
    # print(f"lookup_ranges ranges_out not sorted: {ranges_out}")
    return sorted(ranges_out, key=lambda x: x.source_start)
  
  def _lookup_range(self, range_in: Range) -> list[Range]:
    # print(f"_lookup_range for {range_in}")

    # Whole range is more or less than known ranges, means all values match between source and dest.
    if range_in.source_end_value() < self.ranges[0].source_start or \
       range_in.source_start > self.ranges[-1].source_end_value():
      # print(f"range_in is fully outside known ranges")
      return [Range(
          dest_start=None, 
          source_start=range_in.source_start, 
          num=range_in.num)]

    starts_low = False
    ends_high = False

    # Range in starts less than known ranges
    if range_in.source_start < self.ranges[0].source_start:
      starts_low = True
      # print(f"range_in starts low")
    # Range in ends higher than known ranges
    if range_in.source_end_value() > self.ranges[-1].source_end_value():
      ends_high = True
      # print(f"range_in ends high")

    relevant_ranges = []
    for r in self.ranges:
      # Special case of only one range relevant because it fully covers the range_in
      if r.contains_source(range_in.source_start) and r.contains_source(range_in.source_end_value()):
        # print("Only one relevant range fully contains")
        return [Range(
          dest_start=None, 
          source_start=r.get_dest(range_in.source_start), 
          num=range_in.num)]

      if r.contains_source(range_in.source_start):
        relevant_ranges.append(r)
      elif r.contains_source(range_in.source_end_value()):
        relevant_ranges.append(r)
        break
      elif len(relevant_ranges) > 0 or starts_low:
        relevant_ranges.append(r)

    # print(f"relevant ranges: {relevant_ranges}")

    # At this point we should have all of the relevant ranges that range_in touches and we know if it 
    # starts low or ends high. Now just need to build the output ranges. These will need to do a 
    # mapping for every relevant range and also cover static mapping in between ranges. The output
    # should contain ranges that cover every source value for range_in
    ranges_out = []
    if starts_low:
      num_low = relevant_ranges[0].source_start - range_in.source_start
      ranges_out.append(Range(
        dest_start=None,
        source_start=range_in.source_start,
        num=num_low
      ))
    for i, r in enumerate(relevant_ranges):
      # If range_in fully covers this range, just use it directly
      if range_in.contains_source(r.source_start) and range_in.contains_source(r.source_end_value()):
        ranges_out.append(Range(
          dest_start=None,
          source_start=r.dest_start,
          num=r.num
        ))
        continue

      # If range_in.start is within this range, trim it
      if r.contains_source(range_in.source_start):
        ranges_out.append(Range(
          dest_start=None,
          source_start=r.get_dest(range_in.source_start),
          num=r.source_end() - range_in.source_start,
        ))

      # If range_in.end is within this range, trim it
      if r.contains_source(range_in.source_end_value()):
        ranges_out.append(Range(
          dest_start=None,
          source_start=r.dest_start,
          num=range_in.source_end() - r.source_start,
        ))

      # If there is a gap between this range and the next, fill it
      if i + 1 < len(relevant_ranges):
        range_diff = relevant_ranges[i+1].source_start - relevant_ranges[i].source_end()
        if range_diff > 0:
          ranges_out.append(Range(
            dest_start=None,
            source_start=relevant_ranges[i].source_end(),
            num = range_diff
          ))

    if ends_high:
      num_high = range_in.source_end() - relevant_ranges[-1].source_end()
      ranges_out.append(Range(
        dest_start=None,
        source_start=relevant_ranges[-1].source_end(),
        num=num_high
      ))

    if not ranges_out:
      ranges_out.append(range_in)
    # print(f"ranges out: {ranges_out}")
    return ranges_out

class Almanac:

  def __init__(self, parsed_mappings: ParsedMapping):
    self.maps = {}
    for mapping in parsed_mappings:
      new_map = RangeMap(mapping.source, mapping.dest, mapping.ranges)
      self.maps[new_map.source] = new_map

  def lookup(self, source: Quantity, dest: str) -> Quantity:
    quantity = source
    while quantity.category != dest:
      quantity = self.maps[quantity.category].lookup(quantity)
      # print(quantity)
    return quantity
  
  def lookup_ranges(self, range_in: Range, source: str, dest: str) -> list[Range]:
    cur_source = source
    ranges = [range_in]
    while cur_source != dest:
      print(cur_source)
      print(ranges)
      use_map = self.maps[cur_source]
      cur_source = use_map.destination
      ranges = use_map.lookup_ranges(ranges)
      print(cur_source)
      print(ranges)
      print("--------")
    return ranges


# def part1():
#   seeds, mappings = parse_inputs()
#   almanac = Almanac(mappings)
#   min_value = 1e9
#   for seed in seeds:
#     qty = almanac.lookup(seed, 'location')
#     if qty.value < min_value:
#       min_value = qty.value

#   print(min_value)


# part1()


def part2():
  _, mappings = parse_inputs()
  seeds = parsing.get_numbers_with_separator(str(data_rows[0][6:]))
  seed_ranges = [Range(dest_start=None, source_start=seeds[i], num=seeds[i+1]) for i in range(0, len(seeds), 2)]
  almanac = Almanac(mappings)
  min_value = math.inf
  for r in seed_ranges:
    print("***********")
    print("***********")
    out = almanac.lookup_ranges(r, "seed", "location")
    val = out[0].source_start
    min_value = min(val, min_value)
  print(min_value)
  


part2()