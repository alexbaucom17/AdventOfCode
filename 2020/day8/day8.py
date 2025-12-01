import copy

def load_data(filename):
    with open(filename) as f:
        return [parse_code(line.rstrip()) for line in f]

def parse_code(line):
    inst, arg = line.split()
    return (inst, int(arg))


class Program:

    def __init__(self, code):
        self.code = code
        self.accumulator = 0
        self.instruction_pointer = 0
        self.visited = set()
        self.running = True

    def step(self):

        if self.instruction_pointer == len(self.code):
            self.running = False
            return False

        if not self.running:
            return False

        inst,arg = self.code[self.instruction_pointer]
        if inst == "nop":
            self.instruction_pointer += 1
        elif inst == "acc":
            self.accumulator += arg
            self.instruction_pointer += 1
        elif inst == "jmp":
            self.instruction_pointer += arg

        return True

    def check_for_loop(self):
        if self.instruction_pointer in self.visited:
            return self.accumulator
        else:
            self.visited.add(self.instruction_pointer)
            return None


def find_acc_value_of_loop(code):
    p = Program(code)
    while True:
        status = p.step()
        if status is False:
            return (True, p.accumulator)

        a = p.check_for_loop()
        if a is not None:
            return (False, a)


def find_value_to_change(code):
    for idx in range(len(code)-1, 0, -1):
        inst = code[idx][0]
        if inst == "nop" or inst == "jmp":
            code_copy = copy.copy(code)
            if inst == "nop":
                code_copy[idx] = ("jmp", code_copy[idx][1])
            elif inst == "jmp":
                code_copy[idx] = ("nop", code_copy[idx][1])
            term, a = find_acc_value_of_loop(code_copy)
            if term:
                return a


if __name__ == '__main__':

    sample_data = load_data("day8/sample_input.txt")
    data = load_data("day8/input.txt")

    print(find_acc_value_of_loop(sample_data))
    print(find_value_to_change(data))


