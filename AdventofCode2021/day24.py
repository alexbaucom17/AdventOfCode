import sys
sys.path.append('.')
import aoc
import math

data_rows = aoc.get_input(24, sample=False, index=2).splitlines()

class ALU:

    def __init__(self):
        self.registers = [0,0,0,0]
        self.register_map = {'w': 0, 'x': 1, 'y': 2, 'z': 3}

    def _get_register(self, reg):
        return self.registers[self.register_map[reg]]

    def _get_value(self, val_or_reg):
        if val_or_reg in self.register_map:
            return self._get_register(val_or_reg)
        else:
            return int(val_or_reg)

    def _set_register(self, reg, val):
        self.registers[self.register_map[reg]] = val

    def input(self, register, val):
        self._set_register(register, val)

    def add(self, reg_a, val_or_reg_b):
        val = self._get_register(reg_a) + self._get_value(val_or_reg_b)
        self._set_register(reg_a, val)

    def mul(self, reg_a, val_or_reg_b):
        val = self._get_register(reg_a) * self._get_value(val_or_reg_b)
        self._set_register(reg_a, val)

    def div(self, reg_a, val_or_reg_b):
        val = math.floor(self._get_register(reg_a) / self._get_value(val_or_reg_b))
        self._set_register(reg_a, val)

    def mod(self, reg_a, val_or_reg_b):
        val = self._get_register(reg_a) % self._get_value(val_or_reg_b)
        self._set_register(reg_a, val)

    def eql(self, reg_a, val_or_reg_b):
        val = self._get_register(reg_a) == self._get_value(val_or_reg_b)
        self._set_register(reg_a, int(val))

    def __str__(self):
        s = ""
        for r in ['w','x','y','z']:
            s += f"{r}:{self._get_register(r)} "
        return s


def parse_and_execute(program, inputs):
    alu = ALU()
    input_count = 0
    for line in program:
        parts = line.split()
        inst = parts[0]
        args = parts[1:]

        if inst == "inp":
            if input_count >= len(inputs):
                raise ValueError(f"Attempted to read from index {input_count} of input array which is only of length {len(inputs)}")
            alu.input(args[0], inputs[input_count])
            input_count += 1
        elif inst == "add":
            alu.add(args[0], args[1])
        elif inst == "mul":
            alu.mul(args[0], args[1])
        elif inst == "div":
            alu.div(args[0], args[1])
        elif inst == "mod":
            alu.mod(args[0], args[1])
        elif inst == "eql":
            alu.eql(args[0], args[1])
        else:
            raise ValueError(f"Unsupported instruction type {int}")

        print(f"{line} - {str(alu)}")

    print(f"{inputs} - {str(alu)}")
    return alu._get_register('z') == 0

def testing():
    n = 13579246899999
    nums = [int(c) for c in str(n)]
    valid = parse_and_execute(data_rows, nums)
    print(valid)
testing()

def part1():
    start_num = 99999999999999
    end_num = 99999999991991
    for n in range(start_num, end_num, -1):
        nums = [int(c) for c in str(n)]
        if 0 in nums:
            continue
        valid = parse_and_execute(data_rows, nums)
        if valid:
            print(f"Found valid num: {n}")
            break

# part1()

