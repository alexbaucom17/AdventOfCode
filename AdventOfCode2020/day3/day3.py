
def load_data(filename):
    with open(filename) as f:
        return [[c == '#' for c in line.strip()] for line in f] 

def next_spot(cur_spot, slope, num_cols):
    new_col = (cur_spot[0] + slope[0]) % num_cols
    new_row = cur_spot[1] + slope[1]
    return (new_col, new_row)

def trees_along_slope(data, slope):
    num_cols = len(data[0])
    num_rows = len(data)
    cur_spot = (0,0)
    stops = []
    while cur_spot[1] < num_rows:
        stops.append(data[cur_spot[1]][cur_spot[0]])
        cur_spot = next_spot(cur_spot, slope, num_cols)
    return stops


if __name__ == '__main__':

    sample_data = load_data("day3/sample_input.txt")
    data = load_data("day3/input.txt")

    # part 1
    trees = trees_along_slope(data, (3,1))
    print(sum(trees))

    # part 2
    slopes = ((1,1),(3,1),(5,1),(7,1),(1,2))
    prod = 1
    for s in slopes:
        trees = trees_along_slope(data, s)
        num = sum(trees)
        prod *= num
        print(num)
    print(prod)
    

    