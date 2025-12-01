import itertools
import numpy as np
import time
import copy

def load_data(filename):
    with open(filename,'r') as f:
        positions = []
        for line in f:
            line = line.strip()
            line = line.replace('<','')
            line = line.replace('>','')
            coords = line.split(',')
            p = []
            for c in coords:
                data = c.strip().split('=')
                p.append(data[1])
            positions.append(np.asarray(p,dtype=int))

    return positions


def compute_gravity(moon1, moon2):
    grav_pos_bool = moon1.pos < moon2.pos
    grav_neg_bool = moon1.pos > moon2.pos
    grav1 = np.zeros((3,), dtype=int)
    grav1[grav_pos_bool] = 1
    grav1[grav_neg_bool] = -1
    grav2 = -grav1
    return (grav1, grav2)


def moons_match_starting_positions(moons, starting_positions):
    for idx, m in enumerate(moons):
        if not np.all(m.pos == starting_positions[idx]):
            return False
    return True

def moons_match_starting_velocities(moons):
    for m in moons:
        if not np.all(m.vel == np.array((0,0,0), dtype=int)):
            return False
    return True


class Moon:
    def __init__(self, pos):
        if pos.shape != (3,):
            raise ValueError("Wrong size")
        self.pos = pos
        self.vel = np.zeros((3,), dtype=int)

    def apply_gravity(self, grav):
        self.vel += grav

    def apply_vel(self):
        self.pos += self.vel

    def kinetic_energy(self):
        return np.sum(np.abs(self.vel))
        
    def potential_energy(self):
        return np.sum(np.abs(self.pos))

    def calc_energy(self):
        return self.kinetic_energy() * self.potential_energy()

    def print(self):
        print("pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>".format(self.pos[0], self.pos[1], self.pos[2], self.vel[0], self.vel[1], self.vel[2]))



def simulate_moons_and_compute_energy(starting_positions, n_steps):
    moons = [Moon(copy.copy(pos)) for pos in starting_positions]

    simulate_batch(moons, n_steps, starting_positions)

    print("After {} steps:".format(n_steps))
    for m in moons:
       m.print()
    
    energy = 0
    for m in moons:
        energy += m.calc_energy()
    print("Energy: {}".format(energy))


def simulate_batch(moons, n_steps, starting_positions):
    for n in range(n_steps):
        # Apply gravity
        for m1, m2 in itertools.combinations(moons, 2):
            grav1, grav2 = compute_gravity(m1,m2)
            m1.apply_gravity(grav1)
            m2.apply_gravity(grav2)
        # Apply velocity
        for m in moons:
            m.apply_vel()

        if moons_match_starting_positions(moons, starting_positions) and moons_match_starting_velocities(moons):
            return (True, n+1)
    
    return (False, n_steps)


def grav_for_col(col):
    grav = np.zeros_like(col)
    for c in col:
        grav += 1*(c<col) -1*(c>col)
    return grav

class MoonVectorized:
    def __init__(self, positions):
        if positions.shape != (4,3):
            raise ValueError("Wrong size")
        self.pos = positions
        self.vel = np.zeros((4,3), dtype=int)

    def apply_gravity(self):
        grav = np.apply_along_axis(grav_for_col, 1, self.pos)
        self.vel += grav

    def apply_vel(self):
        self.pos += self.vel

    def print(self):
        for i in self.pos.shape[0]:
            print("pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>".format(self.pos[i,0], self.pos[i,1], self.pos[i,2], self.vel[i,0], self.vel[i,1], self.vel[i,2]))


def find_cycle_time_vectorized(starting_positions, batch_size):
    starting_positions = np.array(starting_positions)
    m = MoonVectorized(copy.copy(starting_positions))

    total_steps = 0
    found = False
    vel_zeros = np.zeros((4,3),dtype=int)
    while True:
        t = time.time()
        for n in range(batch_size):
            m.apply_gravity()
            m.apply_vel()
            if np.all(m.pos == starting_positions) and np.all(m.vel == vel_zeros):
                found = True
                break
        dt = time.time() - t
        total_steps += n
        print("Batch of {} steps took {} seconds".format(batch_size, dt))
        if found:
            print("Found starting state after {} steps".format(total_steps))
            print("Starting state was: ")
            print(starting_positions)
            print("Final state was:")
            m.print()
            return


def find_cycle_time(starting_positions, batch_size):
    moons = [Moon(copy.copy(pos)) for pos in starting_positions]

    total_steps = 0
    while True:
        t = time.time()
        status, steps = simulate_batch(moons, batch_size, starting_positions)
        dt = time.time() - t
        total_steps += steps
        print("Batch of {} steps took {} seconds".format(steps, dt))
        if status:
            print("Found starting state after {} steps".format(total_steps))
            print("Starting state was: ")
            for p in starting_positions:
                print(p)
            print("Final state was:")
            for m in moons:
                m.print()
            return

if __name__ == '__main__':
    
    sample_data1 = load_data("Day12/sample_input1.txt")
    # simulate_moons_and_compute_energy(sample_data1, 10)

    sample_data2 = load_data("Day12/sample_input2.txt")
    # simulate_moons_and_compute_energy(sample_data2, 100)

    # part 1
    data = load_data("Day12/input.txt")
    # simulate_moons_and_compute_energy(data, 1000)

    # part 2
    find_cycle_time(sample_data1, 500)