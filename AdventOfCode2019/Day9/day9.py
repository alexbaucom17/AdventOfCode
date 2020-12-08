import copy



def num_args_for_op(op):
    if op in [1,2,7,8]:
        return 3
    elif op in [5,6]:
        return 2
    elif op in [3,4,9]:
        return 1
    elif op in [99]:
        return 0
    else:
        raise ValueError("Missing n_args for op {}".format(op))

def parse_opcode(op):
    op_digits = num_to_digits(op)

    if len(op_digits) > 1:
        opcode = 10 * op_digits[-2] + op_digits[-1]
    else:
        opcode = op_digits[-1]

    if len(op_digits) > 2:
        parameter_modes = op_digits[:-2]
        parameter_modes = parameter_modes[::-1]
    else:
        parameter_modes = []

    n = num_args_for_op(opcode)
    parameter_modes += [0] * (n-len(parameter_modes))

    return opcode,parameter_modes

def num_to_digits(num):
    digits = []
    div = 10
    while True:
        r = int(num % div)
        digits.append(r)
        num -= r * (div/10)
        num /= 10
        if num < 1:
            break
    
    return digits[::-1]

class IntCode:

    def __init__(self, prog):
        self.prog = copy.copy(prog)
        self.output_buffer = None
        self.input_buffer = None
        self.relative_base = 0
        self.idx = 0
        self.status = 1

    def safe_read(self, arg, parameter_mode):
        if parameter_mode == 0:
            return self.read_prog_data_with_extension(arg)
        elif parameter_mode == 1:
            return arg
        elif parameter_mode == 2:
            return self.read_prog_data_with_extension(self.relative_base + arg)
        else:
            raise ValueError("Invalid parameter mode")

    def safe_write(self, arg, parameter_mode, data):
        #Similar to parse_arg, but always returns the address instead of value
        if parameter_mode == 0:
            self.set_prog_data_with_extension(data, arg)
        elif parameter_mode == 2:
            self.set_prog_data_with_extension(data, self.relative_base + arg)
        else:
            raise ValueError("Invalid parameter mode")

    def read_prog_data_with_extension(self, idx):
        # Allows reading past the end of the size of prog
        if idx >= len(self.prog):
            self.prog.extend([0] * (idx - len(self.prog) + 1))
        return self.prog[idx]

    def set_prog_data_with_extension(self, data, idx):
        if idx >= len(self.prog):
            self.prog.extend([0] * (idx - len(self.prog) + 1))
        self.prog[idx] = data

    def run_prog(self):

        while True:
            op = self.prog[self.idx]
            opcode, modes = parse_opcode(op)

            # Make sure we wait for input if we need it
            if opcode == 3 and self.input_buffer is None:
                self.status = 3
                break

            n_args = num_args_for_op(opcode)
            args = self.prog[self.idx+1:self.idx+1+n_args]
            self.status, rtn = self.do_op(self.prog, opcode, args, modes)
            if self.status == 0:
                break
            elif self.status == -1:
                print('ERROR!')
            elif self.status == 2:
                self.idx = rtn
            else:
                self.idx += n_args+1
                if self.status == 4:
                    break

        return self.status

    def give_input(self, val):
        if self.input_buffer is not None:
            print('WARNING: overwriting existing input value')
        self.input_buffer = val

    def get_output(self):
        out =  copy.copy(self.output_buffer)
        self.output_buffer = None
        return out

    def do_op(self, prog, op, args, parameter_modes):

        # 1 is ok, 0 is end, -1 is error, 2 is return idx, 3 is need input, 4 is have output
        status = 1
        rtn = 0

        if op == 1: # Addition
            a0 = self.safe_read(args[0], parameter_modes[0])
            a1 = self.safe_read(args[1], parameter_modes[1])
            self.safe_write(args[2], parameter_modes[2], a0 + a1)
        elif op == 2: # Multiplication
            a0 = self.safe_read(args[0], parameter_modes[0])
            a1 = self.safe_read(args[1], parameter_modes[1])
            self.safe_write(args[2], parameter_modes[2], a0 * a1)
        elif op == 3: # Input
            val = int(copy.copy(self.input_buffer))
            self.safe_write(args[0], parameter_modes[0], val)
            self.input_buffer = None
        elif op == 4: # Output
            if self.output_buffer is not None:
                print("WARINIG: Overwriting existing output value")
            self.output_buffer = self.safe_read(args[0], parameter_modes[0])
            status = 4
        elif op == 5: # Modify program counter on True
            a0 = self.safe_read(args[0], parameter_modes[0])
            a1 = self.safe_read(args[1], parameter_modes[1])
            if a0 != 0:
                rtn = a1
                status = 2
        elif op == 6: # Modify program counter on False
            a0 = self.safe_read(args[0], parameter_modes[0])
            a1 = self.safe_read(args[1], parameter_modes[1])
            if a0 == 0:
                rtn = a1
                status = 2
        elif op == 7: # Less than comparison
            a0 = self.safe_read(args[0], parameter_modes[0])
            a1 = self.safe_read(args[1], parameter_modes[1])
            if a0 < a1:
                self.safe_write(args[2], parameter_modes[2], 1)
            else:
                self.safe_write(args[2], parameter_modes[2], 0)
        elif op == 8: # Equality comparison
            a0 = self.safe_read(args[0], parameter_modes[0])
            a1 = self.safe_read(args[1], parameter_modes[1])
            if a0 == a1:
                self.safe_write(args[2], parameter_modes[2], 1)
            else:
                self.safe_write(args[2], parameter_modes[2], 0)
        elif op == 9: # Modify relative base
            self.relative_base += self.safe_read(args[0], parameter_modes[0])
        elif op == 99:
            status = 0
        else:
            status = -1

        return status,rtn


def run_prog_with_input(prog, input):

    p = IntCode(prog)
    running = True

    while running:
        status = p.run_prog()
        if status == 3:
            p.give_input(input)
        elif status == 4:
            print(p.get_output())
        elif status == 0 or status == -1:
            running = False


def test_1():
    text = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    prog_str = text.split(',')
    prog = [int(x) for x in prog_str]
    run_prog_with_input(prog,0)

def test_2():
    text = "1102,34915192,34915192,7,4,7,99,0"
    prog_str = text.split(',')
    prog = [int(x) for x in prog_str]
    run_prog_with_input(prog,0)

def test_3():
    text = "104,1125899906842624,99"
    prog_str = text.split(',')
    prog = [int(x) for x in prog_str]
    run_prog_with_input(prog,0)

def main():
    with open('Day9/input.txt','r') as f:
        text = f.read()
        prog_str = text.split(',')
        prog = [int(x) for x in prog_str]
        run_prog_with_input(prog,1)

def main2():
    with open('Day9/input.txt','r') as f:
        text = f.read()
        prog_str = text.split(',')
        prog = [int(x) for x in prog_str]
        run_prog_with_input(prog,2)

if __name__ == '__main__':
    main2()