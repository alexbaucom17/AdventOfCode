import math


def compute_fuel(mass):
    a = mass / 3.0
    b = math.floor(a)
    c = b - 2
    return c

def compute_all_fuel(mass):
     # Get inital fuel calculation
    fuel = compute_fuel(mass)
    total = 0
    while fuel > 0:
        total += fuel
        fuel = compute_fuel(fuel)
    return total



if __name__ == '__main__':


    # Example values
    for x in [12, 14, 1969, 100756]:
        print(compute_all_fuel(x))

    # Actual input
    total = 0
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            total += compute_all_fuel(int(line))

    print(total)
