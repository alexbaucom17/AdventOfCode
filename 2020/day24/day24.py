import numpy as np
import copy
import matplotlib.pyplot as plt

diag = np.array((0.5, 0.5*np.sqrt(3)))
hz = np.array((1.0,0))

def load_data(filename):
    with open(filename) as f:
        data = []
        for line in f:
            tmp_char = None
            tmp_data = []
            for c in line.strip():
                if tmp_char is not None:
                    tmp_data.append(tmp_char+c)
                    tmp_char = None
                elif c in ('e','w'):
                    tmp_data.append(c)
                else:
                    tmp_char = c
            
            data.append(tmp_data)

        return data


def hex_move(pos, d):
    new_pos = None
    if d == 'e':
        new_pos = pos + hz
    elif d == 'w':
        new_pos = pos - hz
    elif d == 'ne':
        new_pos = pos + diag
    elif d == 'se':
        new_pos = pos + np.array((1.0,-1.0)) * diag
    elif d == 'sw':
        new_pos = pos + np.array((-1.0,-1.0)) * diag
    elif d == 'nw':
        new_pos = pos + np.array((-1.0,1.0)) * diag
    return new_pos


def locate_tile(path):
    pos = np.array((0.0,0.0))
    for p in path:
        pos = hex_move(pos, p)
    return pos

def flip_tiles(data):
    tiles = {}
    for path in data:
        exact_pos = locate_tile(path)
        key_pos = truncate_and_tuple(exact_pos)

        any_key_match = None
        for check_key in tiles.keys():
            if check_key_match(key_pos, check_key):
                any_key_match = check_key
                break
        
        if any_key_match:
            tiles[any_key_match]["state"] = not tiles[any_key_match]["state"]
        else:
            tiles[key_pos] = {"state": False, "exact": exact_pos}

    return tiles


def count_black_tiles(tiles):
    count = 0
    for v in tiles.values():
        if v["state"] is False:
            count += 1

    return count

def truncate_and_tuple(x):
    num_places = 2
    y = np.floor( x * (10**2)) / 10**2
    return tuple(y)

def count_adjacent_black_tiles(pos, tiles):

    count = 0
    for d in ['e', 'w', 'se', 'sw', 'ne', 'nw']:
        neighbor_pos = truncate_and_tuple(hex_move(pos, d))
        for check_key in tiles.keys():
            if check_key_match(neighbor_pos, check_key) and tiles[check_key]["state"] is False:
                count += 1

    return count

def check_key_match(k1, k2):
    eps = 0.1
    if abs(k1[0] - k2[0]) < eps and abs(k1[1] - k2[1])  < eps:
        return True
    return False

def expand_tiles(tiles):
    new_tiles = copy.copy(tiles)
    for key_pos,data in tiles.items():
        color = data["state"]
        exact_pos = data["exact"]
        if color == False:
            for d in ['e', 'w', 'se', 'sw', 'ne', 'nw']:
                neighbor_exact_pos = hex_move(exact_pos, d)
                neighbor_key_pos = truncate_and_tuple(neighbor_exact_pos)
                any_neighbor_match = False
                for check_key in new_tiles.keys():
                    if check_key_match(neighbor_key_pos, check_key):
                        any_neighbor_match = True
                        break
                if not any_neighbor_match:
                    new_tiles[neighbor_key_pos] = {"state": True, "exact": neighbor_exact_pos}
    return new_tiles


def flip_tiles_for_day(tiles):

    tiles = expand_tiles(tiles)
    # print("N tiles: {}".format(len(tiles)))
    # draw_tiles(tiles, "After expansion")
    new_tiles = copy.deepcopy(tiles)
    for key_pos,data in tiles.items():
        color = data["state"]
        exact_pos = data["exact"]
        adjacent_black_tiles = count_adjacent_black_tiles(exact_pos, tiles)
        if color is False and (adjacent_black_tiles == 0 or adjacent_black_tiles > 2):
            new_tiles[key_pos]["state"] = True
        elif color is True and adjacent_black_tiles == 2:
            new_tiles[key_pos]["state"] = False
    return new_tiles


def simulate_n_days(data, n):

    tiles = flip_tiles(data)
    # draw_tiles(tiles, "After initial flip")
    for i in range(n):
        tiles = flip_tiles_for_day(tiles)
        n_black = count_black_tiles(tiles)
        print("Day {}: {}".format(i+1, n_black))
        # draw_tiles(tiles, "End of day")

def draw_tiles(tiles, title):

    x = []
    y = []
    c = []
    for key_pos, data in tiles.items():
        x.append(key_pos[0])
        y.append(key_pos[1])
        if data["state"]:
            c.append("cyan")
        else:
            c.append("black")

    fig, ax = plt.subplots()
    plt.scatter(x,y,s=1000, c=c,marker='h', edgecolors="white")
    ax.set_aspect("equal")
    ax.set_xlim((-5,5))
    ax.set_ylim((-5,5))
    ax.set_title(title)
    plt.show()



if __name__ == '__main__':

    sample_data = load_data("day24/sample_input.txt")
    data = load_data("day24/input.txt") 

    debug_data = [["e"],["sw"],['e','w']]

    # Part 1
    # tiles = flip_tiles(sample_data)
    # for t,v in tiles.items():
    #     print("{}:{}".format(t,v))
    # print(count_black_tiles(tiles))

    # Part 2
    simulate_n_days(data, 100)