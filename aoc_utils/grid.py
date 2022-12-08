from dataclasses import dataclass, field, astuple
from typing import Any
import queue
import math
import time
import numpy as np

@dataclass(frozen=True)
class Coord:
    row: int
    col: int

@dataclass(frozen=True)
class Point:
    x: int
    y: int

def ortho_neighbors():
    return ((-1,0),(0,-1),(1,0),(0,1))

def ortho_diag_neighbors():
    return ((-1,0),(0,-1),(1,0),(0,1),(1,1),(-1,1),(1,-1),(-1,-1)) 

def cost_at_point(grid, coord):
    return grid.safe_get(coord)
class Grid:
    def __init__(self, data: list[list[int]]):
        self.data = data
        self.n_rows = len(data)
        self.n_cols = len(data[0])

    def safe_get(self, coord: Coord, invalid=None):
        if coord.row < 0 or coord.row >= self.n_rows or coord.col < 0 or coord.col >= self.n_cols:
            return invalid
        else:
            return self.data[coord.row][coord.col]

    def safe_get_point(self, point: Point, invalid=None):
        if point.y < 0 or point.y >= self.n_rows or point.x < 0 or point.x >= self.n_cols:
            return invalid
        else:
            return self.data[point.y][point.x] 

    def numpy(self):
        return np.asarray(self.data)

    def get_neighbors(self, coord: Coord, neighbor_fn=ortho_neighbors):
        neighbors = []
        for dcoord in neighbor_fn():
            check_coord = Coord(coord.row+dcoord[0], coord.col+dcoord[1])
            val = self.safe_get(check_coord)
            if val is not None:
                neighbors.append((check_coord,val))
        return neighbors

    def __str__(self):
        out = ""
        for row in self.data:
            for val in row:
                out += str(val)
            out += "\n"
        return out

@dataclass(frozen=True, order=True)
class SearchNode:
    sort_cost: int
    coord: Coord=field(compare=False)
    path: tuple[Coord]=field(compare=False)
    actual_cost: int=field(compare=False)

def dijkstra_cost_fn(cur_node: SearchNode, neighbor_coord: Coord, neighbor_cost: int, end: Coord):
    return cur_node.actual_cost + neighbor_cost

def astar_cost_fn(cur_node: SearchNode, neighbor_coord: Coord, neighbor_cost: int, end: Coord):
    prev_cost = cur_node.actual_cost + neighbor_cost
    est_cost = abs(end.row - neighbor_coord.row) + abs(end.col - neighbor_coord.col)
    return prev_cost + est_cost

def find_path(start: Coord, end: Coord, grid: Grid, neighbor_fn=ortho_neighbors, cost_fn=astar_cost_fn):
        tic = time.perf_counter()
        q = queue.PriorityQueue()
        explored = set()
        q.put(SearchNode(sort_cost=0, coord=start, path=(start,), actual_cost=0))

        while not q.empty():
            node = q.get()
            # print(f"{node.sort_cost}, {node.actual_cost}, {node.coord}")

            if node.coord == end:
                toc = time.perf_counter()
                print(f"Search time: {toc - tic:0.4f} seconds, Total nodes explored: {len(explored)}")
                return (node.actual_cost, node.path)

            neighbors = grid.get_neighbors(node.coord, neighbor_fn)
            for n_coord, n_cost in neighbors:
                if n_coord not in explored:
                    new_sort_cost = cost_fn(node, n_coord, n_cost, end)
                    new_actual_cost = node.actual_cost + n_cost
                    new_path = node.path + (n_coord,)
                    q.put(SearchNode(sort_cost=new_sort_cost, coord=n_coord, path=new_path, actual_cost=new_actual_cost))
            explored.add(node.coord)

        toc = time.perf_counter()
        print(f"Search time: {toc - tic:0.4f} seconds, Total nodes explored: {len(explored)}")
        return (-1, None)