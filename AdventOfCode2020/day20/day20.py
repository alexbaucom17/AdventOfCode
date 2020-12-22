import numpy as np
import queue
import cProfile

def load_data(filename):
    with open(filename) as f:
        tiles = {}
        id = None
        tile_data = []
        for line in f:
            line = line.strip()
            if line == "":
                tiles[id] = TileDescriptor(id, np.array(tile_data, dtype=bool))
                id = None
                tile_data = []
            elif line.startswith("Tile"):
                line = line.replace("Tile ","")
                line = line.replace(":","")
                id = int(line)
            else:
                tile_data.append([c == '#' for c in line])

        tiles[id] = TileDescriptor(id, np.array(tile_data, dtype=bool))
        return tiles

def reverse_mask(x):
    x = ((x & 0x55555555) << 1) | ((x & 0xAAAAAAAA) >> 1)
    x = ((x & 0x33333333) << 2) | ((x & 0xCCCCCCCC) >> 2)
    x = ((x & 0x0F0F0F0F) << 4) | ((x & 0xF0F0F0F0) >> 4)
    x = ((x & 0x00FF00FF) << 8) | ((x & 0xFF00FF00) >> 8)
    x = ((x & 0x0000FFFF) << 16) | ((x & 0xFFFF0000) >> 16)
    return x

class TileDescriptor:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        edge_len = self.data.shape[0]
        self.edge_data = np.concatenate([self.data[0,:].reshape((1,edge_len)), \
                                         self.data[:,0].reshape((1,edge_len)), \
                                         self.data[-1,:].reshape((1,edge_len)), \
                                         self.data[:,-1].reshape((1,edge_len))])
        self.top_edge = 0
        self.left_edge = 1
        self.bottom_edge = 2
        self.right_edge = 3
        self.connections = {"Left": None, "Right": None, "Top": None, "Bottom": None}

    def flipud(self):
        tmp = self.top_edge
        self.top_edge = self.bottom_edge
        self.bottom_edge = tmp
        self.edge_data[self.left_edge,:] = np.flip(self.edge_data[self.left_edge,:])
        self.edge_data[self.right_edge,:] = np.flip(self.edge_data[self.right_edge,:])
        
    def fliplr(self):
        tmp = self.right_edge
        self.right_edge = self.left_edge
        self.left_edge = tmp
        self.edge_data[self.top_edge,:] = np.flip(self.edge_data[self.top_edge,:])
        self.edge_data[self.bottom_edge,:] = np.flip(self.edge_data[self.bottom_edge,:])

    def rotateccw(self):
        self.edge_data[self.top_edge,:] = np.flip(self.edge_data[self.top_edge,:])
        self.edge_data[self.bottom_edge,:] = np.flip(self.edge_data[self.bottom_edge,:])
        self.top_edge = (self.top_edge - 1) % 4
        self.left_edge = (self.left_edge - 1) % 4
        self.bottom_edge = (self.bottom_edge - 1) % 4
        self.right_edge = (self.right_edge - 1) % 4

    def rotatecw(self):
        self.edge_data[self.right_edge,:] = np.flip(self.edge_data[self.right_edge,:])
        self.edge_data[self.left_edge,:] = np.flip(self.edge_data[self.left_edge,:])
        self.top_edge = (self.top_edge + 1) % 4
        self.left_edge = (self.left_edge + 1) % 4
        self.bottom_edge = (self.bottom_edge + 1) % 4
        self.right_edge = (self.right_edge + 1) % 4

    def get_edge(self, dir):
        if dir == "Left":
            return self.get_left_edge()
        elif dir == "Right":
            return self.get_right_edge()
        elif dir == "Top":
            return self.get_top_edge()
        elif dir == "Bottom":
            return self.get_bottom_edge()
        else:
            raise ValueError("Unknown dir")

    def get_top_edge(self):
        return self.edge_data[self.top_edge,:]

    def get_left_edge(self):
        return self.edge_data[self.left_edge,:]

    def get_bottom_edge(self):
        return self.edge_data[self.bottom_edge,:]

    def get_right_edge(self):
        return self.edge_data[self.right_edge,:]


def try_tile_join_fixed(new_id, fixed_id, join_dir, tiles):

    fixed_tile = tiles[fixed_id]
    new_tile = tiles[new_id]

    new_dir = ""
    if join_dir == "Left":
        new_dir = "Right"
    elif join_dir == "Right":
        new_dir = "Left"
    elif join_dir == "Top":
        new_dir = "Bottom"
    elif join_dir == "Bottom":
        new_dir = "Top"

    fixed_edge = fixed_tile.get_edge(join_dir)
    new_edge = new_tile.get_edge(new_dir)

    if np.all(fixed_edge == new_edge):
        fixed_tile.connections[join_dir] = new_id
        new_tile.connections[new_dir] = fixed_id
        return True
    else:
        return False

def try_tile_join_all_perms(new_id, fixed_id, join_dir, tiles):

    fixed_tile = tiles[fixed_id]
    new_tile = tiles[new_id]
    for i in range(4):
        joined = try_tile_join_fixed(new_id, fixed_id, join_dir, tiles)
        if joined:
            return True
        else:
            new_tile.rotateccw()
    
    new_tile.fliplr()
    for i in range(4):
        joined = try_tile_join_fixed(new_id, fixed_id, join_dir, tiles)
        if joined:
            return True
        else:
            new_tile.rotateccw()

    return False


def check_tile_fit(tile_id, fixed_id, tiles):

    fixed_tile = tiles[fixed_id]
    joined = False
    for join_dir,val in fixed_tile.connections.items():
        # print("Checking dir: {}".format(join_dir))
        if val:
            # print("Fixed id {} already joined with {} along {} direction".format(fixed_id, val, join_dir))
            continue
        joined = try_tile_join_all_perms(tile_id, fixed_id, join_dir, tiles)
        if joined:
            break
    return joined

def add_tile_to_grid(tile_id, assembled, tiles):

    fit = False
    for fixed_id in assembled:
        # print("Checking fit with fixed tile: {}".format(fixed_id))
        fit = check_tile_fit(tile_id, fixed_id, tiles)
        if fit:
            assembled.append(tile_id)
            break
    return fit


def assemble_tiles(tiles):

    all_keys = [k for k in tiles.keys()]
    assembled = [all_keys[0]]
    unused = queue.Queue()
    for k in all_keys[1:]:
        unused.put(k)

    count = 0
    while not unused.empty() and count < 100:
        count += 1
        tile_id = unused.get()
        # print("Checking new tile: {}".format(tile_id))
        fit = add_tile_to_grid(tile_id, assembled, tiles)
        # print("Fit: {}".format(fit))
        if not fit:
            # print("No fit found, adding {} to end of queue".format(tile_id))
            unused.put(tile_id)

    return assembled

def insert_into_grid_with_expansion(grid, pos, id):
    pad_dir = [[0,0], [0,0]]
    new_pos = np.copy(pos)
    if pos[0] < 0:
        pad_dir[0][0] = 1
        new_pos += np.array([1, 0])
    elif pos[0] >= grid.shape[0]:
        pad_dir[0][1] = 1
    elif pos[1] < 0:
        pad_dir[1][0] = 1
        new_pos += np.array([0, 1])
    elif pos[1] >= grid.shape[1]:
        pad_dir[1][1] = 1

    # print(pad_dir)
    grid = np.pad(grid, pad_dir, mode='constant', constant_values=0)
    # print(grid)
    grid[new_pos[0], new_pos[1]] = id
    return grid


def create_grid_from_tile_connections(assembled, tiles):
    grid = np.array([assembled[0]]).reshape((1,1))
    ids_to_check = queue.Queue()
    ids_to_check.put(assembled[0])
    already_checked = set()

    while not ids_to_check.empty():
        id = ids_to_check.get()
        already_checked.add(id)
        tile_to_check = tiles[id]
        for join_dir,val in tile_to_check.connections.items():
            if not val:
                continue
            if val in already_checked:
                continue
            grid_pos_split = np.where(grid == id)
            grid_pos = np.array([grid_pos_split[0][0], grid_pos_split[1][0]])
            # print(grid_pos)
            move_pos = None
            if join_dir == "Right":
                move_pos = np.array([0,1])
            elif join_dir == "Left":
                move_pos = np.array([0,-1])
            elif join_dir == "Top":
                move_pos = np.array([-1,0])
            elif join_dir == "Bottom":
                move_pos = np.array([1,0])

            insert_pos = grid_pos + move_pos
            # print("Inserting {} at pos {}".format(val, insert_pos))
            grid = insert_into_grid_with_expansion(grid, insert_pos, val)
            # print(grid)
            ids_to_check.put(val)

    return grid

def multiply_corners(grid):
    n1 = int(grid[0,0])
    n2 = int(grid[0, grid.shape[1]-1])
    n3 = int(grid[grid.shape[0]-1, 0])
    n4 = int(grid[grid.shape[0]-1, grid.shape[1]-1])
    return n1*n2*n3*n4



if __name__ == '__main__':

    sample_data = load_data("day20/sample_input.txt")
    data = load_data("day20/input.txt") 

    # tiles = data
    # cProfile.run('assembled_ids = assemble_tiles(tiles)')
    # print(assembled_ids)

    # cProfile.run('grid = create_grid_from_tile_connections(assembled_ids, tiles)')
    # print(grid)

    # print(multiply_corners(grid))


    x = int('11001100',2)
    print('{0:b}'.format(x))
    print('{0:b}'.format(reverse_mask(x)))


    # print(check_tile_fit(1427, 2729, sample_data))


    # for tile in sample_data.values():
    #     print("Tile:\n{}\n".format(tile.data))
    #     print("Top:\n{}\n".format(tile.get_top_edge()))
    #     print("Bottom:\n{}\n".format(tile.get_bottom_edge()))
    #     tile.rotateccw()
    #     print("Top:\n{}\n".format(tile.get_top_edge()))
    #     print("Bottom:\n{}\n".format(tile.get_bottom_edge()))
    #     print("Left:\n{}\n".format(tile.get_left_edge()))
    #     print("Right:\n{}\n".format(tile.get_right_edge()))
    #     tile.rotatecw()
    #     print("Left:\n{}\n".format(tile.get_left_edge()))
    #     print("Right:\n{}\n".format(tile.get_right_edge()))
    #     break
    