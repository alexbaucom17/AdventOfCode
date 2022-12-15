from operator import itemgetter

# This takes a list of pairs (a, b) describing a range and merges all ranges together into the 
# minimum set of unique ranges that cover all input ranges.
def merge_1d_ranges(ranges):

  # If there is only one range, just return it
  if len(ranges) == 1:
    return [tuple(ranges[0])]

  # Attach id to each number and sort (num, id) pairs
  tmp_ranges = []
  id = 0
  for r in ranges:
    tmp_ranges.append((r[0], id))
    tmp_ranges.append((r[1], id))
    id += 1
  sorted_ranges = sorted(tmp_ranges, key=itemgetter(0))

  # Now we need to loop through the sorted values and figure out which ones can be grouped together.
  # There's complicated logic to handle various edge cases and duplicated values, but this loop
  # will only take a single pass through sorted_ranges so is O(N).
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
          # If set is empty but next slot(s) have same number, add this id and continue looping
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
        # If the open_id set is not empty after removing the next id, we are still in the same range
        # just continue.
        continue
    else:
      # If the id is not in our set of ids, this is the start of a new sub-range, so add it to the 
      # open_id set
      open_id.add(next_id)
  
  return merged_ranges