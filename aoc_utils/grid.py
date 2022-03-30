from dataclasses import dataclass

@dataclass(frozen=True)
class Coord:
    row: int
    col: int

@dataclass(frozen=True)
class Point:
    x: int
    y: int

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

def ortho_neighbors():
    return ((-1,0),(0,-1),(1,0),(0,1))

def ortho_diag_neighbors():
    return ((-1,0),(0,-1),(1,0),(0,1),(1,1),(-1,1),(1,-1),(-1,-1)) 

def get_neighbors(coord: Coord, mat: list[list[int]], neighbor_fn=ortho_neighbors):
    neighbors = []
    g = Grid(mat)
    for dcoord in neighbor_fn():
        check_coord = Coord(coord.row+dcoord[0], coord.col+dcoord[1])
        val = g.safe_get(check_coord)
        if val is not None:
            neighbors.append((check_coord,val))
    return neighbors