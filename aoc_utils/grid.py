from dataclasses import dataclass

@dataclass(frozen=True)
class Coord:
    row: int
    col: int

def safe_get(coord, mat):
    if coord.row < 0 or coord.row >= len(mat) or coord.col < 0 or coord.col >= len(mat[0]):
        return None
    else:
        return mat[coord.row][coord.col]

def ortho_neighbors():
    return ((-1,0),(0,-1),(1,0),(0,1))

def ortho_diag_neighbors():
    return ((-1,0),(0,-1),(1,0),(0,1),(1,1),(-1,1),(1,-1),(-1,-1)) 

def get_neighbors(coord: Coord, mat: list[list[int]], neighbor_fn=ortho_neighbors):
    neighbors = []
    for dcoord in neighbor_fn():
        check_coord = Coord(coord.row+dcoord[0], coord.col+dcoord[1])
        val = safe_get(check_coord, mat)
        if val is not None:
            neighbors.append((check_coord,val))
    return neighbors