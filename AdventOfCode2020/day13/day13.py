def load_data(filename):
    with open(filename) as f:
        data = [line.rstrip() for line in f]
        timestamp = int(data[0])
        buses = [c for c in data[1].split(',')]
        return timestamp, buses

def condense_buses(buses):
    return [int(b) for b in buses if b != 'x']

def any_bus_arrives(time, buses):
    for b in buses:
        if time % b == 0:
            return b
    return None

def find_next_bus(timestamp, buses):
    buses = condense_buses(buses)
    count = 1
    while True:
        check_time = timestamp + count
        print("Checking time: {}".format(check_time))
        b = any_bus_arrives(check_time, buses)
        if b is not None:
            print("Found bus: {} after {} minues. Answer: {}".format(b, count, b*count))
            return
        count += 1



if __name__ == '__main__':

    sample_data = load_data("day13/sample_input.txt")
    data = load_data("day13/input.txt") 

    find_next_bus(data[0], data[1])