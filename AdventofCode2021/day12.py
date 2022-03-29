from cgitb import small
import sys
sys.path.append('.')
import aoc
import queue
import math

data_rows = aoc.get_input(12, sample=False).splitlines()

def parse_rows():
    rows = []
    for row in data_rows:
        v1,v2 = row.split("-")
        rows.append((v1,v2))
    return rows

def build_edge_dict(edges):
    ed = {}
    for v1,v2 in edges:
        for x,y in [(v1,v2),(v2,v1)]:
            if x in ed:
                ed[x].add(y)
            else:
                ed[x] = {y}
    return ed

def part1():
    rows = parse_rows()
    ed = build_edge_dict(rows)
    search_queue = queue.Queue()
    search_queue.put((["start"],"start", False))
    finished_paths = []

    while not search_queue.empty():
        cur_path, cur_node, small_dup = search_queue.get()
        neighbors = ed[cur_node]
        for n in neighbors:
            if n == "end":
                finished_paths.append(cur_path+[n])
            elif n.islower():
                if n in cur_path:
                    if small_dup or n == "start":
                        continue
                    else:
                        search_queue.put((cur_path+[n],n,True))
                else:
                    search_queue.put((cur_path+[n],n,small_dup))
            else:
                search_queue.put((cur_path+[n],n,small_dup))

    # for p in finished_paths:
    #     print(p)

    print(len(finished_paths))

part1()
