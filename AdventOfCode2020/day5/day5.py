
def load_data(filename):
    with open(filename) as f:
        return [line.rstrip() for line in f] 

def binary_search(pattern, size):
    low = 1
    hi = size + 1
    split = int(hi / 2)
    for p in pattern:
        if p:
            low = split
        else:
            hi = split
        split = int((hi - low) / 2) + low
    return hi - 1
            
def row_col_for_pass(boarding_pass):
    row_pattern = [c == "B" for c in boarding_pass[:7]]
    col_pattern = [c == "R" for c in boarding_pass[7:]]
    row = binary_search(row_pattern, 127)
    col = binary_search(col_pattern, 7)
    return (row, col)

def get_id(bp):
    row, col = row_col_for_pass(bp)
    id = row * 8 + col
    return id

def find_max_id(data):
    max_id = 0
    for bp in data:
        id = get_id(bp)
        if id > max_id:
            max_id = id
    return max_id

def find_missing_seat(data):
    ids = []
    for bp in data:
        ids.append(get_id(bp))

    ids.sort()
    counter = ids[0]
    for id in ids:
        if counter != id:
            return counter
        counter += 1
    
    return -1


if __name__ == '__main__':

    sample_data = load_data("day5/sample_input.txt")
    data = load_data("day5/input.txt")

    for bp in sample_data:
        print(row_col_for_pass(bp))

    # part 1
    print(find_max_id(data))

    # part 2
    print(find_missing_seat(data))