import numpy as np
import math

def load_data(filename):
    with open(filename) as f:
        data = [line.rstrip() for line in f]
        return data

class Pose:
    def __init__(self, x, a):
        self.x = np.array(x).reshape((2,1))
        self.a = np.array(a).reshape((2,1))

    def forward(self, units):
        self.x += self.a * units

    def north(self, units):
        self.x += np.array([0,1]).reshape((2,1)) * units

    def south(self, units):
        self.x += np.array([0,-1]).reshape((2,1)) * units

    def east(self, units):
        self.x += np.array([1,0]).reshape((2,1)) * units

    def west(self, units):
        self.x += np.array([-1,0]).reshape((2,1)) * units

    def rotate(self, units):
        u_rad = math.radians(units)
        mat = np.round(np.array([[math.cos(u_rad), -1*math.sin(u_rad)], \
                        [math.sin(u_rad),    math.cos(u_rad)]]))


        self.a = np.matmul(mat, self.a)

    def update(self, instruction):
        i = instruction[0]
        d = int(instruction[1:])
        if i == 'N':
            self.north(d)
        elif i == 'S':
            self.south(d)
        elif i == 'E':
            self.east(d)
        elif i == 'W':
            self.west(d)
        elif i == 'F':
            self.forward(d)
        elif i == 'L':
            self.rotate(d)
        elif i == 'R':
            self.rotate(-1*d)
        else:
            raise ValueError("Unknown command: {}".format(instruction))

        # print("Instruction: {}".format(instruction))
        # print(self.x.reshape((1,2)))
        # print(self.a.reshape((1,2))) 


def calc_position_from_instructions(data):
    p = Pose((0.0,0.0), (1.0,0.0))
    for instruction in data:
        p.update(instruction)
    print(np.sum(np.abs(p.x)))


class PoseWithWaypoint:
    def __init__(self, x, w):
        self.x = np.array(x).reshape((2,1))
        self.w = np.array(w).reshape((2,1))

    def forward(self, units):
        self.x += units * self.w

    def north(self, units):
        self.w += np.array([0,1]).reshape((2,1)) * units

    def south(self, units):
        self.w += np.array([0,-1]).reshape((2,1)) * units

    def east(self, units):
        self.w += np.array([1,0]).reshape((2,1)) * units

    def west(self, units):
        self.w += np.array([-1,0]).reshape((2,1)) * units

    def rotate(self, units):
        u_rad = math.radians(units)
        mat = np.round(np.array([[math.cos(u_rad), -1*math.sin(u_rad)], \
                        [math.sin(u_rad),    math.cos(u_rad)]]))

        self.w = np.matmul(mat, self.w)

    def update(self, instruction):
        i = instruction[0]
        d = int(instruction[1:])
        if i == 'N':
            self.north(d)
        elif i == 'S':
            self.south(d)
        elif i == 'E':
            self.east(d)
        elif i == 'W':
            self.west(d)
        elif i == 'F':
            self.forward(d)
        elif i == 'L':
            self.rotate(d)
        elif i == 'R':
            self.rotate(-1*d)
        else:
            raise ValueError("Unknown command: {}".format(instruction))

        print("Instruction: {}".format(instruction))
        print(self.x.reshape((1,2)))
        print(self.w.reshape((1,2))) 

def calc_position_from_instructions_with_waypoint(data):
    p = PoseWithWaypoint((0.0,0.0), (10.0,1.0))
    for instruction in data:
        p.update(instruction)
    print(np.sum(np.abs(p.x)))


if __name__ == '__main__':

    sample_data = load_data("day12/sample_input.txt")
    data = load_data("day12/input.txt") 

    # calc_position_from_instructions(data)

    calc_position_from_instructions_with_waypoint(data)