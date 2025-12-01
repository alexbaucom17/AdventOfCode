import numpy as np
import math

def load_data(filename):
    with open(filename,'r') as f:
        return np.asarray([[c == '#' for c in line.rstrip()] for line in f])

def has_asteroid(data, col_row):
    return data[col_row[1], col_row[0]]

def in_bounds(data, point):
    num_cols = data.shape[1]
    num_rows = data.shape[0]
    col = point[0]
    row = point[1]
    ok = True
    ok &= col >= 0
    ok &= row >= 0
    ok &= col < num_cols
    ok &= row < num_rows
    return ok

def normalize_direction(vector):
    f = math.gcd(vector[0], vector[1])
    if f > 1:
        vector = vector / f
    return vector.astype(int)

def first_asteroid_along_vector(data, start, vector):

    check_point = start
    while True:
        check_point = check_point + vector
        if not in_bounds(data, check_point):
            return None
        elif has_asteroid(data, check_point):
            return check_point

def get_all_direction_vectors(data_size):
    all_vectors_raw = [ np.asarray(tuple((x,y))) for y in range(-data_size[1]+1, data_size[1]) for x in range(-data_size[0]+1,data_size[0])]
    all_vectors_norm = set()
    for vec in all_vectors_raw:
        all_vectors_norm.add(tuple(normalize_direction(vec)))
    all_vectors_norm.remove((0,0))
    return all_vectors_norm

def get_asteroids_seen_from_point(data, start):
    found = set()
    for dir in get_all_direction_vectors(data.shape):
        vec = np.asarray(dir)
        point = first_asteroid_along_vector(data, start, vec)
        if point is not None:
            found.add(tuple(point))
    return found

def sort_all_directions(directions):
    dirs_sorted = sorted(directions, key=lambda dir: math.atan2(dir[1], dir[0]))
    idx = dirs_sorted.index((0,-1))
    return dirs_sorted[idx:] + dirs_sorted[:idx]

def find_locaiton_of_max_asteroids(data):
    points = np.argwhere(data)
    points[:,[0,1]] = points[:,[1,0]]
    max_asteroids = 0
    max_idx = None
    for point in points:
        num_seen = len(get_asteroids_seen_from_point(data, point))
        #print("Found {} at {}".format(num_seen, point))
        if num_seen > max_asteroids:
            max_asteroids = num_seen
            max_idx = point
    print("Max is {} at {}".format(max_asteroids, max_idx))
    return (max_asteroids, max_idx)

def vaporize(data, start, direction):
    asteroid = first_asteroid_along_vector(data, start, direction)
    if asteroid is not None:
        data[asteroid[1], asteroid[0]] = False
    return (data, asteroid)

def find_nth_vaporization(data, location, n):
    dirs = sort_all_directions(get_all_direction_vectors(data.shape))
    count = 0
    while count < n:
        for dir in dirs:
            data, asteroid = vaporize(data, location, dir)
            if asteroid is not None:
                count += 1
                #print("Asteroid {} is {}".format(count, asteroid))
            if count == n:
                return asteroid
    return None

def find_200th_vaporization_from_max_station(data):
    _, location = find_locaiton_of_max_asteroids(data)
    return find_nth_vaporization(data, location, 200)

if __name__ == '__main__':

    # sample_data1 = load_data("Day10/sample_input1.txt")
    # sample_data2 = load_data("Day10/sample_input2.txt")
    # sample_data3 = load_data("Day10/sample_input3.txt")
    # sample_data4 = load_data("Day10/sample_input4.txt")
    sample_data5 = load_data("Day10/sample_input5.txt")
    data = load_data("Day10/input.txt")

    # part 1
    # find_locaiton_of_max_asteroids(sample_data1)
    # find_locaiton_of_max_asteroids(sample_data2)
    # find_locaiton_of_max_asteroids(sample_data3)
    # find_locaiton_of_max_asteroids(sample_data4)
    # find_locaiton_of_max_asteroids(sample_data5)
    # find_locaiton_of_max_asteroids(data)

    # part 2
    sample_data6 = load_data("Day10/sample_input6.txt")
    #print(find_nth_vaporization(sample_data6, np.asarray((8,3)), 36))
    x,y = find_200th_vaporization_from_max_station(data)
    print(x*100 + y)
