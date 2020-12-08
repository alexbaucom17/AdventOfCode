import Intcode


def run_to_next_output(p):
    while True:
        status = p.run_prog()
        if status == 3:
            raise RuntimeError("Input expected")
        elif status == 4:
            return p.get_output()
        elif status == 0 or status == -1:
            return None

def run_robot(prog, start_color):
    location = [0,0]
    direction_idx = 0
    directions = [[0,1],[1,0],[0,-1],[-1,0]]
    painted = {tuple(location): start_color}
    p = Intcode.IntCode(prog)
    
    while True:
        # Get the color at the current location
        color = 0
        if tuple(location) in painted.keys():
            color = painted[tuple(location)]
        p.give_input(color)
        
        # first output is color to paint
        output = run_to_next_output(p)
        if output is None:
            return painted
        else:
            painted[tuple(location)] = output
            # print("Painting {} as {}".format(location, output))

        # second output is turn direction
        output = run_to_next_output(p)
        if output is None:
            return painted
        else:
            if output is 0:
                direction_idx = (direction_idx - 1) % 4
            elif output is 1:
                direction_idx = (direction_idx + 1) % 4
            location[0] += directions[direction_idx][0]
            location[1] += directions[direction_idx][1]
            # print("Moved to {}".format(location))

import numpy as np
from matplotlib import pyplot as plt
def decode_painting(paint_map):
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    for key in painted.keys():
        if key[0] < min_x:
            min_x = key[0]
        if key[0] > max_x:
            max_x = key[0]
        if key[1] < min_y:
            min_y = key[1]
        if key[1] > max_y:
            max_y = key[1]

    shift_amount = np.asarray([-min_x, - min_y])
    bounds = np.asarray([max_x+1, max_y+1]) + shift_amount
    print(shift_amount)
    print((max_x, max_y))
    print(bounds)
    I = np.zeros(bounds)
    for key,val in painted.items():
        if val:
            I[key[0]+shift_amount[0], key[1]+shift_amount[1]] = 1

    binary = np.flipud(np.transpose(I)) > 0
    plt.imshow(binary)
    plt.show()
        

if __name__ == '__main__':
    prog = Intcode.load_prog_from_file("Day11/intcode_prog.txt")

    # part 1
    painted = run_robot(prog, 0)
    print(len(painted))

    # part 2
    painted = run_robot(prog, 1)
    decode_painting(painted)