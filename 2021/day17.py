import sys
sys.path.append('.')
import aoc
import math
import numpy as np
from enum import Enum

# Real input
target_x = np.asarray([128, 160])
target_y = np.asarray([-142, -88])

# Example
# target_x = np.asarray([20, 30])
# target_y = np.asarray([-10, -5])

def step(pos: np.array, vel: np.array) -> tuple([np.array, np.array]):
    out_pos = pos + vel
    x_sign = 0 if vel[0] == 0 else 1 if vel[0] > 0 else -1
    out_vel = vel + np.asarray([-x_sign, -1])
    return out_pos, out_vel

def pos_in_target_area(pos: np.array) -> bool:
    if pos[0] >= target_x[0] and pos[0] <= target_x[1] and pos[1] >= target_y[0] and pos[1] <= target_y[1]:
        return True
    return False

class SimStatus(Enum):
    MAX_STEPS = 1
    IN_TARGET = 2
    MISSED_SHORT = 3
    MISSED_LONG = 4
    MISSED_VERTICAL = 5

def simulate(vel0: np.array, max_steps: int) -> SimStatus:
    pos = np.asarray([0,0])
    vel = vel0
    for i in range(max_steps):
        pos, vel = step(pos, vel)
        # print(f"After step {i}: pos ({pos[0]},{pos[1]}), vel ({vel[0]},{vel[1]})")
        if pos[0] > target_x[1]:
            return SimStatus.MISSED_LONG
        if pos[1] < target_y[0]:
            if pos[0] < target_x[0]:
                return SimStatus.MISSED_SHORT
            else:
                return SimStatus.MISSED_VERTICAL
        if pos_in_target_area(pos):
            # print(f"Reached target area at ({pos[0]},{pos[1]}) after {i+1} steps.")
            return SimStatus.IN_TARGET

    # print(f"Did not reach target area after {i+1} steps. Final pos: {pos[0]},{pos[1]})")
    return SimStatus.MAX_STEPS

def find_max_height(v0: np.array) -> int:
    max_height = 0
    pos = np.asarray([0,0])
    vel = v0
    while True:
        pos, vel = step(pos, vel)
        if pos[1] > max_height:
            max_height = pos[1]
        else:
            break

    return max_height

def test_simulation():
    example_velocities = [[7,2], [6,3], [9,0], [17, -4]]
    for v in example_velocities:
        simulate(np.asarray(v), 10)

def part1():
    vel = np.asarray([1,1])
    best_v = np.copy(vel)
    max_height = 0
    max_steps = 1000
    miss_vertical_count = 0
    dy_target = abs(target_y[0] - target_y[1]) 
    while True:
        status = simulate(vel, max_steps)
        if status == SimStatus.IN_TARGET:
            height = find_max_height(vel)
            if height > max_height:
                max_height = height
                best_v = np.copy(vel)
            vel[1] += 1
        elif status == SimStatus.MAX_STEPS:
            raise ValueError(f"Reached max steps for vel: {vel}")
        elif status == SimStatus.MISSED_LONG:
            vel[0] -= 1
            if vel[0] <= 0:
                break
        elif status == SimStatus.MISSED_SHORT:
            vel[0] += 1
        elif status == SimStatus.MISSED_VERTICAL:
            vel[1] += 1
            miss_vertical_count += 1
            if miss_vertical_count > dy_target:
                break

    print(f"Found max height of {max_height} with starting vel {best_v}")

# part1()


def part2():

    vx_bounds = [0, target_x[1] + 5]
    vy_bounds = [target_y[0], 200]
    max_steps = 1000
    n_valid = 0

    for vx in range(vx_bounds[0], vx_bounds[1]):
        for vy in range(vy_bounds[0], vy_bounds[1]):
            status = simulate(np.asarray([vx, vy]), max_steps)
            if status == SimStatus.IN_TARGET:
                n_valid += 1
            elif status == SimStatus.MAX_STEPS:
                raise ValueError(f"Reached max steps for vel: {vx},{vy}")

    print(n_valid)
part2()



