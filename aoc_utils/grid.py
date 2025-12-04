from dataclasses import dataclass, field, astuple
from typing import Any
import queue
import copy
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
    
    def safe_set(self, coord: Coord, value):
        if coord.row < 0 or coord.row >= self.n_rows or coord.col < 0 or coord.col >= self.n_cols:
           return
        self.data[coord.row][coord.col] = value

    def __str__(self):
        out = ""
        for row in self.data:
            for val in row:
                out += str(val)
            out += "\n"
        return out
    
    def str_dot_hash(self):
        out = ""
        for row in self.data:
            for val in row:
                out += "." if val == 0 else "#"
            out += "\n"
        return out
      


def grid_from_str(rows: list[str], empty_str: str=".", occ_str: str = "#") -> Grid:
    int_grid = []
    for row in rows:
        int_row = []
        for c in row:
            if c == empty_str:
                int_row.append(0)
            elif c == occ_str:
              int_row.append(1)
            else:
              raise ValueError(f"Found char {c} which does not match empty char ({empty_str}) or occ char ({occ_str})")
        int_grid.append(int_row)
    return Grid(int_grid)
       
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

def grid_is_cost(grid, coord, neighbor_steps=ortho_neighbors):
    return grid.get_neighbors(coord, neighbor_steps)

def print_search(grid: Grid, path: list[Coord], explored: set[Coord]):
    step_map = {(-1,0): "<", (1,0): ">", (0,-1): "^", (0,1): "V"}
    char_grid = [["." for _ in row] for row in grid.numpy()]
    for c in explored:
        char_grid[c.row][c.col] = "-"
    for i in range(len(path)-1):
        step_row = path[i+1].row - path[i].row
        step_col = path[i+1].col - path[i].col
        char_grid[path[i].row][path[i].col] = step_map[(step_col, step_row)]
    char_grid[path[-1].row][path[-1].col]= "E"
    for row in char_grid:
        print("".join(row))


def find_path(start: Coord, end: Coord, grid: Grid, neighbor_fn=grid_is_cost, cost_fn=astar_cost_fn):
        tic = time.perf_counter()
        q = queue.PriorityQueue()
        explored = set()
        q.put(SearchNode(sort_cost=0, coord=start, path=(start,), actual_cost=0))

        while not q.empty():
            node = q.get()
            # print(f"{node.coord}, {node.sort_cost}, {node.actual_cost}")

            if node.coord in explored:
                continue

            if node.coord == end:
                toc = time.perf_counter()
                # print(f"Search time: {toc - tic:0.4f} seconds, Total nodes explored: {len(explored)}")
                # print_search(grid, node.path, explored)
                return (node.actual_cost, node.path)

            neighbors = neighbor_fn(grid, node.coord)
            for n_coord, n_cost in neighbors:
                if n_coord not in explored:
                    new_sort_cost = cost_fn(node, n_coord, n_cost, end)
                    new_actual_cost = node.actual_cost + n_cost
                    new_path = node.path + (n_coord,)
                    q.put(SearchNode(sort_cost=new_sort_cost, coord=n_coord, path=new_path, actual_cost=new_actual_cost))
            explored.add(node.coord)

        toc = time.perf_counter()
        # print(f"Search time: {toc - tic:0.4f} seconds, Total nodes explored: {len(explored)}")
        return (-1, None)


class ExpandingGrid:
  def __init__(self, init_offset_x=500, init_offset_y=500, default_val=None):
    self.data = [[default_val for x in range(2)] for y in range(2)]
    self.x_offset = init_offset_x
    self.y_offset = init_offset_y
    self.default_val = default_val

  def x_lims(self):
    return (self.x_offset, self.x_offset + len(self.data[0]))

  def y_lims(self):
    return (self.y_offset, self.y_offset + len(self.data))

  def get(self, point: Point):
    if self._in_lims(point):
      return self.data[point.y-self.y_offset][point.x-self.x_offset] 
    else:
      return self.default_val

  def get_oob(self, point: Point, oob_val=None):
    if self._in_lims(point):
      return self.data[point.y-self.y_offset][point.x-self.x_offset] 
    else:
      return oob_val

  def _in_lims(self, point: Point):
    x_lims = self.x_lims()
    y_lims = self.y_lims()
    if point.y < y_lims[0] or point.y >= y_lims[1] or point.x < x_lims[0] or point.x >= x_lims[1]:
      return False
    else:
      return True
  
  def set(self, point: Point, val):
    if self._in_lims(point):
      self._fixed_set(point, val)
    else:
      self._expand_set(point, val)

  def _fixed_set(self, point: Point, val):
    y = point.y-self.y_offset
    x = point.x-self.x_offset
    self.data[y][x] = val

  def _expand_set(self, point: Point, val):
    cur_x_lim = self.x_lims()
    cur_y_lim = self.y_lims()
    new_x_lim = list(copy.deepcopy(cur_x_lim))
    new_y_lim = list(copy.deepcopy(cur_y_lim))
    if point.y < cur_y_lim[0]:
      new_y_lim[0] = point.y - 1
    if point.y >= cur_y_lim[1]:
      new_y_lim[1] = point.y + 1
    if point.x < cur_x_lim[0]:
      new_x_lim[0] = point.x - 1
    if point.x >= cur_x_lim[1]:
      new_x_lim[1] = point.x + 1

    cur_dx = cur_x_lim[1] - cur_x_lim[0]
    cur_dy = cur_y_lim[1] - cur_y_lim[0]
    new_dx = new_x_lim[1] - new_x_lim[0]
    new_dy = new_y_lim[1] - new_y_lim[0]
    new_data = [[self.default_val for x in range(new_dx)] for y in range(new_dy)]
    new_to_cur_x = cur_x_lim[0] - new_x_lim[0]
    new_to_cur_y = cur_y_lim[0] - new_y_lim[0]
    for x in range(cur_dx):
      for y in range(cur_dy):
        new_data[new_to_cur_y + y][new_to_cur_x + x] = self.data[y][x]
    self.data = new_data
    
    self.x_offset = new_x_lim[0]
    self.y_offset = new_y_lim[0]
    self._fixed_set(point, val)