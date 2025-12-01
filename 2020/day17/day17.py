import numpy as np

def load_data(filename):
    with open(filename) as f:
        data = np.array([[True if c == '#' else False for c in line.rstrip()] for line in f])
        return data


def count_active_neighbors(grid, idx):
    minx = max(idx[0] - 1, 0)
    miny = max(idx[1] - 1, 0)
    minz = max(idx[2] - 1, 0)
    maxx = min(idx[0] + 2, grid.shape[0])
    maxy = min(idx[1] + 2, grid.shape[1])
    maxz = min(idx[2] + 2, grid.shape[2])
    region = grid[minx:maxx, miny:maxy, minz:maxz]
    # print("Region:\n{}\n".format(region))
    # print("Sum:\n{}\n".format(np.sum(region)))
    # print("Grid:\n{}\n".format(int(grid[idx[0], idx[1], idx[2]])))
    return np.sum(region) - int(grid[idx[0], idx[1], idx[2]])


def upscale_grid(grid):
    idx = np.where(grid)
    pads = [[0,0], [0,0], [0,0]]
    for i in [0,1,2]:
        if np.min(idx[i]) == 0:
            pads[i][0] = 1
        if np.max(idx[i]) == grid.shape[i]-1:
            pads[i][1] = 1

    return np.pad(grid, pads, mode='constant', constant_values=False)


def run_cycle(grid):
    new_grid = np.copy(grid)

    for i in range(new_grid.shape[0]):
        for j in range(new_grid.shape[1]):
            for k in range(new_grid.shape[2]):
                n_active = count_active_neighbors(grid, (i,j,k))
                if grid[i, j, k] and not (n_active == 2 or n_active == 3):
                    new_grid[i, j, k] = False
                elif not grid[i, j, k] and n_active == 3:
                    new_grid[i, j, k] = True

    return upscale_grid(new_grid)

def count_active_after_initialization(data):
    grid = upscale_grid(data.reshape((1, data.shape[0], data.shape[1])))
    for i in range(6):
        grid = run_cycle(grid)

    print(np.sum(grid))


def count_active_neighbors_4d(grid, idx):
    minx = max(idx[0] - 1, 0)
    miny = max(idx[1] - 1, 0)
    minz = max(idx[2] - 1, 0)
    minw = max(idx[3] - 1, 0)
    maxx = min(idx[0] + 2, grid.shape[0])
    maxy = min(idx[1] + 2, grid.shape[1])
    maxz = min(idx[2] + 2, grid.shape[2])
    maxw = min(idx[3] + 2, grid.shape[3])
    region = grid[minx:maxx, miny:maxy, minz:maxz, minw:maxw]
    return np.sum(region) - int(grid[idx[0], idx[1], idx[2], idx[3]])


def upscale_grid_4d(grid):
    idx = np.where(grid)
    pads = [[0,0], [0,0], [0,0], [0,0]]
    for i in [0,1,2,3]:
        if np.min(idx[i]) == 0:
            pads[i][0] = 1
        if np.max(idx[i]) == grid.shape[i]-1:
            pads[i][1] = 1

    return np.pad(grid, pads, mode='constant', constant_values=False)


def run_cycle_4d(grid):
    new_grid = np.copy(grid)

    for i in range(new_grid.shape[0]):
        for j in range(new_grid.shape[1]):
            for k in range(new_grid.shape[2]):
                for w in range(new_grid.shape[3]):
                    n_active = count_active_neighbors_4d(grid, (i,j,k,w))
                    if grid[i, j, k, w] and not (n_active == 2 or n_active == 3):
                        new_grid[i, j, k, w] = False
                    elif not grid[i, j, k, w] and n_active == 3:
                        new_grid[i, j, k, w] = True

    return upscale_grid_4d(new_grid)

def count_active_after_initialization_4d(data):
    grid = upscale_grid_4d(data.reshape((1, data.shape[0], data.shape[1], 1)))
    for i in range(6):
        grid = run_cycle_4d(grid)

    print(np.sum(grid))

if __name__ == '__main__':

    sample_data = load_data("day17/sample_input.txt")
    data = load_data("day17/input.txt")

    using_data = data
    
    #part 1
    count_active_after_initialization(using_data)
    
    # part 2
    count_active_after_initialization_4d(using_data)


    