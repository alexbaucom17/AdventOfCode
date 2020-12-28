import numpy as np
import queue
import cProfile
import random

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


class TileDescriptor:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        edge_len = self.data.shape[0]
        self.edge_data = [  ''.join(['1' if i else '0' for i in self.data[0,:]]),
                            ''.join(['1' if i else '0' for i in self.data[:,0]]),
                            ''.join(['1' if i else '0' for i in self.data[-1,:]]),
                            ''.join(['1' if i else '0' for i in self.data[:,-1]])]
        self.top_edge = 0
        self.left_edge = 1
        self.bottom_edge = 2
        self.right_edge = 3
        self.connections = {"Left": None, "Right": None, "Top": None, "Bottom": None}
        self.rot_val = 1
        self.mutations = []

    def flipud(self):
        tmp = self.top_edge
        self.top_edge = self.bottom_edge
        self.bottom_edge = tmp
        self.edge_data[self.left_edge] = self.edge_data[self.left_edge][::-1]
        self.edge_data[self.right_edge] = self.edge_data[self.right_edge][::-1]
        self.rot_val = -1*self.rot_val
        self.mutations.append("ud")
        
    def fliplr(self):
        tmp = self.right_edge
        self.right_edge = self.left_edge
        self.left_edge = tmp
        self.edge_data[self.top_edge] = self.edge_data[self.top_edge][::-1]
        self.edge_data[self.bottom_edge] = self.edge_data[self.bottom_edge][::-1]
        self.rot_val = -1*self.rot_val
        self.mutations.append("lr")

    def rotateccw(self):
        self.edge_data[self.top_edge] = self.edge_data[self.top_edge][::-1]
        self.edge_data[self.bottom_edge] = self.edge_data[self.bottom_edge][::-1]
        self.top_edge = (self.top_edge - self.rot_val) % 4
        self.left_edge = (self.left_edge - self.rot_val) % 4
        self.bottom_edge = (self.bottom_edge - self.rot_val) % 4
        self.right_edge = (self.right_edge - self.rot_val) % 4
        self.mutations.append("ccw")

    def rotatecw(self):
        self.edge_data[self.right_edge] = self.edge_data[self.right_edge][::-1]
        self.edge_data[self.left_edge] = self.edge_data[self.left_edge][::-1]
        self.top_edge = (self.top_edge + self.rot_val) % 4
        self.left_edge = (self.left_edge + self.rot_val) % 4
        self.bottom_edge = (self.bottom_edge + self.rot_val) % 4
        self.right_edge = (self.right_edge + self.rot_val) % 4
        self.mutations.append("cw")

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
        return self.edge_data[self.top_edge]

    def get_left_edge(self):
        return self.edge_data[self.left_edge]

    def get_bottom_edge(self):
        return self.edge_data[self.bottom_edge]

    def get_right_edge(self):
        return self.edge_data[self.right_edge]

    def print_edges(self):
        arr = np.zeros(self.data.shape, dtype=int)
        arr[0,:] = [int(c) for c in self.edge_data[self.top_edge]]
        arr[-1,:] = [int(c) for c in self.edge_data[self.bottom_edge]]
        arr[:,0] = [int(c) for c in self.edge_data[self.left_edge]]
        arr[:,-1] = [int(c) for c in self.edge_data[self.right_edge]]
        print(arr)

    def get_data(self):
        d = np.copy(self.data)
        for m in self.mutations:
            if m == "ud":
                d = np.flipud(d)
            elif m == "lr":
                d = np.fliplr(d)
            elif m == "cw":
                d = np.rot90(d, -1)
            elif m == "ccw":
                d = np.rot90(d, 1)
        return d

    def get_data_no_borders(self):
        d = self.get_data()
        return d[1:-1, 1:-1]



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

    if int(fixed_edge, 2) == int(new_edge, 2):
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
    random.shuffle(all_keys)
    assembled = [all_keys[0]]
    unused = queue.Queue()
    for k in all_keys[1:]:
        unused.put(k)

    count = 0
    while not unused.empty():
        if count % 100 == 0:
            print("Count: {}, num unused: {}".format(count, unused.qsize()))
        count += 1
        tile_id = unused.get()
        # print("Checking new tile: {}".format(tile_id))
        fit = add_tile_to_grid(tile_id, assembled, tiles)
        # print("Fit: {}".format(fit))
        if not fit:
            # print("No fit found, adding {} to end of queue".format(tile_id))
            unused.put(tile_id)

        if count > 1000:
            break

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


def assemble_image(grid, tiles):
    grid_size = grid.shape
    all_keys = [k for k in tiles.keys()]
    tile_size = tiles[all_keys[0]].get_data_no_borders().shape

    assembled_size = (grid_size[0] * tile_size[0], grid_size[1] * tile_size[1])
    img = np.zeros(assembled_size, dtype=bool)

    for r,row in enumerate(grid):
        for c,id in enumerate(row):
            img_r_start = r * tile_size[0]
            img_r_end = img_r_start + tile_size[0]
            img_c_start = c * tile_size[1]
            img_c_end = img_c_start + tile_size[1]
            img[img_r_start:img_r_end, img_c_start:img_c_end] = tiles[id].get_data_no_borders()

    return img


monster_pattern = tuple([[0,18],[1,0],[1,5],[1,6],[1,11],[1,12],[1,17],[1,18],[1,19],[2,1],[2,4],[2,7],[2,10],[2,13],[2,16]])
def is_monster_present(img_section):
    for coord in monster_pattern:
        if not img_section[coord[0], coord[1]]:
            return False
    return True

def search_for_monsters(img):
    sub_grid_size = (3,20)
    img_size = img.shape
    row_searches = img_size[0] - sub_grid_size[0]
    col_searches = img_size[1] - sub_grid_size[1]

    n_monsters = 0
    for r in range(row_searches):
        for c in range(col_searches):
            section = img[r:r+sub_grid_size[0], c:c+sub_grid_size[1]]
            if is_monster_present(section):
                n_monsters += 1
    return n_monsters

def search_for_monsters_all_orientations(img):

    n_monsters = 0
    for i in range(2):
        for j in range(4):
            n_monsters = search_for_monsters(img)
            if n_monsters > 0:
                return n_monsters
            img = np.rot90(img)
        img = np.fliplr(img)
    return n_monsters


if __name__ == '__main__':

    sample_data = load_data("day20/sample_input.txt")
    data = load_data("day20/input.txt") 
    random.seed(0)

    tiles = data
    assembled_ids = assemble_tiles(tiles)

    grid = create_grid_from_tile_connections(assembled_ids, tiles)
    np.set_printoptions(edgeitems=30, linewidth=100000)
    print(grid)

    # Part 1
    print(multiply_corners(grid))

    # Part 2
    img = assemble_image(grid, tiles)
    # print(img)
    n_monsters = search_for_monsters_all_orientations(img)
    print(n_monsters)
    n_points_for_monsters = n_monsters * len(monster_pattern)
    n_all_points = np.sum(img)
    print(n_all_points - n_points_for_monsters)

    