import numpy as np
import cProfile

def load_data(filename):
    with open(filename) as f:
        data = [[int(c == 'L') for c in line.rstrip()] for line in f]
        return np.array(data)


neighbor_cache = {}
def get_neighbors(coord):
    if coord in neighbor_cache.keys():
        return neighbor_cache[coord]
    n = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            n.append(coord + np.array([i,j]))
    neighbor_cache[coord] = n
    return n

neighbor_direction_cache = {}
def get_neighbors_visible(coord, data):
    if coord in neighbor_direction_cache.keys():
        return neighbor_direction_cache[coord]
    
    dirs = [ (i,j) for i in [-1, 0, 1] for j in [-1, 0, 1]]
    dirs.remove((0,0))
    neighbors = []
    for d in dirs:
        check_coord = np.copy(np.array(coord))
        while True:
            check_coord = check_coord + np.array(d);
            if check_coord[0] >= 0 and check_coord[0] < data.shape[0] and check_coord[1] >=0 and check_coord[1] < data.shape[1]:
                if data[check_coord[0], check_coord[1]] != 0:
                    neighbors.append(tuple(check_coord))
                    break
            else:
                break
    neighbor_direction_cache[coord] = neighbors
    return neighbors


def count_neighbors_full_with_limits(data, neighbors):
    num_full = 0
    for n in neighbors:
        if n[0] >= 0 and n[0] < data.shape[0] and n[1] >=0 and n[1] < data.shape[1]:
            num_full += int(data[n[0], n[1]] == 2)
    return num_full

def sim_one_step(seats_idx, seat_data):
    prev_seat_data = np.copy(seat_data)
    for idx in seats_idx:
        # part 1
        # neighbors = get_neighbors(idx)
        # part 2
        neighbors = get_neighbors_visible(idx, seat_data)
        neighbors_full = count_neighbors_full_with_limits(prev_seat_data, neighbors)
        if prev_seat_data[idx] == 2 and neighbors_full >= 5:  # part 1: 4
            seat_data[idx] = 1
        elif prev_seat_data[idx] == 1 and neighbors_full == 0:
            seat_data[idx] = 2

    changed = np.any(seat_data != prev_seat_data)
    return (changed, seat_data)
            
def get_seat_idx(data):
    seats_idx = []
    elems = np.nonzero(data != 0)
    for i in range(len(elems[0])):
        seats_idx.append((elems[0][i], elems[1][i]))
    return seats_idx

def simulate_seats(data):
    all_seats_idx = get_seat_idx(data)
    count = 0
    while True:
        print("Loop: {}".format(count)) 
        count += 1
        changed, data = sim_one_step(all_seats_idx, data)
        if not changed:
            print(np.sum(np.sum(data == 2)))
            return


if __name__ == '__main__':

    sample_data = load_data("day11/sample_input.txt")
    data = load_data("day11/input.txt") 

    simulate_seats(data)
    #print(get_neighbors_visible((0,2), sample_data))