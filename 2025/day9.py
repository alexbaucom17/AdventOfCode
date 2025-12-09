
import sys
sys.path.append('.')
import aoc
from aoc_utils import parsing

data_rows = aoc.get_input(day=9, sample=False, index=0).splitlines()
points = list(map(lambda row: parsing.get_numbers_with_separator(row, ","), data_rows))

def area(p1, p2): 
  dx = abs(p1[0] - p2[0]) + 1
  dy = abs(p1[1] - p2[1]) + 1
  return dx * dy

def part1():
  best = 0
  for i in range(len(points) - 1):
    for j in range(i+1, len(points)):
      p1 = points[i]
      p2 = points[j]
      best = max(best, area(p1, p2))
  print(f"Best: {best}")
  print(f"Checked {sum([i for i in range(len(points))])} rectangles")

# part1()

def build_edges(points):
  hz_edges = []
  vt_edges = []
  for i in range(len(points)):
    p1 = points[i]
    if i == len(points) - 1:
      p2 = points[0]
    else:
      p2 = points[i+1]
    
    if p1[0] == p2[0]:
      ys = sorted([p1[1], p2[1]])
      vt_edges.append((ys[0], ys[1], p1[0]))
    if p1[1] == p2[1]:
      xs = sorted([p1[0], p2[0]])
      hz_edges.append((xs[0], xs[1], p1[1]))

  return hz_edges, vt_edges

# def build_check_fn(points):
#   hz_edges, vt_edges = build_edges(points)
#   # print("hz edges")
#   # for e in hz_edges:
#   #   print(e)
#   # print("vt edges")
#   # for e in vt_edges:
#   #   print(e)

#   def on_or_inside(point):
#     for edge in hz_edges:
#       if edge[0] <= point[0] <= edge[1] and point[1] == edge[2]:
#         # print(f"{point} on hz edge {edge}")
#         return True
#     for edge in vt_edges:
#       if edge[0] <= point[1] <= edge[1] and point[0] == edge[2]:
#         # print(f"{point} on vt edge {edge}")
#         return True

#     count = 0
#     for edge in vt_edges:
#       if edge[0] <= point[1] < edge[1] and point[0] < edge[2]:
#         count += 1
#     # print(f"{point} count {count}")
#     return count % 2 == 1
#   return on_or_inside

def build_check_fn_ai(points):
    hz_edges, vt_edges = build_edges(points)

    # --- POINT TEST ---
    def on_or_inside(point):
        x, y = point

        # On horizontal edge
        for x1, x2, ey in hz_edges:
            if ey == y and x1 <= x <= x2:
                return True

        # On vertical edge
        for y1, y2, ex in vt_edges:
            if ex == x and y1 <= y <= y2:
                return True

        # Ray cast to the right
        count = 0
        for y1, y2, ex in vt_edges:
            if y1 <= y < y2 and x < ex:
                count += 1

        return (count % 2) == 1

    # --- SEGMENT TEST ---
    # segment is axis-aligned; check that *every integer point* is inside
    def segment_inside(a, b):
        ax, ay = a
        bx, by = b

        # Endpoints must be valid
        if not (on_or_inside(a) and on_or_inside(b)):
            return False

        # vertical segment
        if ax == bx:
            x = ax
            y0, y1 = sorted([ay, by])

            # Check intersection with horizontal edges
            for x0, x1, yh in hz_edges:
                if x0 < x < x1 and y0 < yh < y1:
                    # genuine crossing
                    # print("found hz crossing")
                    return False

            # # Check overlap with vertical edges
            # for y0e, y1e, xe in vt_edges:
            #     if xe == x and not (y1 < y0e or y0 > y1e):
            #         # Overlapping boundary segment
            #         # interior test: move 1 cell right
            #         test_point = (x - 1, (max(y0, y0e) + min(y1, y1e)) // 2)
            #         if not on_or_inside(test_point):
            #             # print(f"failed test point {test_point}")
            #             return False

            return True

        # horizontal segment
        if ay == by:
            y = ay
            x0, x1 = sorted([ax, bx])

            # intersections w/ vertical edges
            for y0, y1, xv in vt_edges:
                if y0 < y < y1 and x0 < xv < x1:
                    # print("Found vt crossing")
                    return False

            # # overlap with horizontal edges
            # for x0e, x1e, yh in hz_edges:
            #     if yh == y and not (x1 < x0e or x0 > x1e):
            #         # Overlapping boundary segment
            #         test_point = ((max(x0, x0e) + min(x1, x1e)) // 2, y - 1)
            #         if not on_or_inside(test_point):
            #             # print(f"failed test point {test_point}")
            #             return False

            return True

        raise ValueError("Segment not axis-aligned")

    return on_or_inside, segment_inside

def is_valid(p1, p2, on_or_inside, segment_inside):
  p3 = (p1[0], p2[1])
  p4 = (p2[0], p1[1])
  if not on_or_inside(p3):
    # print(f"{p3} not valid")
    return False
  if not on_or_inside(p4):
    # print(f"{p4} not valid")
    return False
  
  # Now check the box edges:
  # (p1 -> p3), (p3 -> p2), (p2 -> p4), (p4 -> p1)

  if not segment_inside(p1, p3):
    # print(f"Edge {p1}, {p3} not valid")
    return False
  if not segment_inside(p3, p2):
    # print(f"Edge {p3}, {p2} not valid")
    return False
  if not segment_inside(p2, p4):
    # print(f"Edge {p2}, {p4} not valid")
    return False
  if not segment_inside(p4, p1):
    # print(f"Edge {p4}, {p1} not valid")
    return False

  return True

def part2():
  on_or_inside, segment_inside = build_check_fn_ai(points)
  
  best = 0
  for i in range(len(points) - 1):
    for j in range(i+1, len(points)):
      p1 = points[i]
      p2 = points[j]
      # print(f"Checking {p1}, {p2}")
      if is_valid(p1, p2, on_or_inside, segment_inside):
        a = area(p1, p2)
        if a > best:
          print(f"Best area {a} for {p1}, {p2}")
          best = a
  print(f"Best: {best}")
  print(f"Checked {sum([i for i in range(len(points))])} rectangles")
  

part2()

