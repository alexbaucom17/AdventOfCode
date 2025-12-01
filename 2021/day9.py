import sys
sys.path.append('.')
import aoc
import queue

data_rows = aoc.get_input(9, sample=False).splitlines()
data_mat = [[int(i) for i in row] for row in data_rows]

def safe_get(i, j, mat):
    if i < 0 or i >= len(mat) or j < 0 or j >= len(mat[0]):
        return None
    else:
        return mat[i][j]

def get_neighbors(i, j, mat):
    vals = []
    dirs = [[-1,0],[0,-1],[1,0],[0,1]]
    for di, dj in dirs:
        # print(f"Checking {i+di},{j+dj}")
        val = safe_get(i+di, j+dj, mat)
        if val is not None:
            vals.append(((i+di,j+dj),val))

    return vals

def get_low_points(mat):
    lows = []
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            # print(f"Searching point ({i},{j})")
            vals = get_neighbors(i, j, data_mat)
            # print(vals)
            cur = safe_get(i, j, data_mat)
            is_low = True
            for coord, v in vals:
                if v <= cur:
                    is_low = False
                    break
            if is_low:
                # print(f"Found low point at ({i},{j}) with height {cur}")
                lows.append(((i,j), cur))
    return lows


def part1():
    lows = get_low_points(data_mat)
    low_vals = [v for _,v in lows]
    risk = len(low_vals) + sum(low_vals)
    print(risk)

part1()

def basin_search(start, mat):
    q = queue.Queue()
    explored = set()
    q.put(start)
    # print('-------------')
    # print(start)

    while not q.empty():
        # print('*****')
        coord = q.get()
        # print(coord)
        nexts = get_neighbors(coord[0], coord[1], mat)
        # print(nexts)

        for c, v in nexts:
            if c not in explored and v < 9:
                q.put(c)
        explored.add(coord)
        # print(explored)

    return len(explored)

def part2():
    lows = get_low_points(data_mat)
    sizes = []
    for c,_ in lows:
        s = basin_search(c, data_mat)
        sizes.append(s)
        print(f"Coord {c} has basin size of {s}")

    sorted_sizes = sorted(sizes, reverse=True)
    print(sorted_sizes[0] * sorted_sizes[1] * sorted_sizes[2])

part2()


