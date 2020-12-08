import copy
import itertools



def parse_arg(prog, arg, parameter_mode):
    if parameter_mode == 0:
        return prog[arg]
    else:
        return arg

def num_args_for_op(op):
    if op in [1,2,7,8]:
        return 3
    elif op in [5,6]:
        return 2
    elif op in [3,4]:
        return 1
    else:
        return 0

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
        self.prog = prog
        self.output_buffer = None
        self.input_buffer = None
        self.idx = 0
        self.status = 1

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
        if op == 1:
            a0 = parse_arg(prog,args[0], parameter_modes[0])
            a1 = parse_arg(prog,args[1], parameter_modes[1])
            prog[args[2]] = a0 + a1
        elif op == 2:
            a0 = parse_arg(prog,args[0], parameter_modes[0])
            a1 = parse_arg(prog,args[1], parameter_modes[1])
            prog[args[2]] = a0 * a1
        elif op == 3:
            prog[args[0]] = int(copy.copy(self.input_buffer))
            self.input_buffer = None
        elif op == 4:
            a0 = parse_arg(prog,args[0], parameter_modes[0])
            if self.output_buffer is not None:
                print("WARINIG: Overwriting existing output value")
            self.output_buffer = a0
            status = 4
        elif op == 5:
            a0 = parse_arg(prog,args[0], parameter_modes[0])
            a1 = parse_arg(prog,args[1], parameter_modes[1])
            if a0 != 0:
                rtn = a1
                status = 2
        elif op == 6:
            a0 = parse_arg(prog,args[0], parameter_modes[0])
            a1 = parse_arg(prog,args[1], parameter_modes[1])
            if a0 == 0:
                rtn = a1
                status = 2
        elif op == 7:
            a0 = parse_arg(prog,args[0], parameter_modes[0])
            a1 = parse_arg(prog,args[1], parameter_modes[1])
            if a0 < a1:
                prog[args[2]] = 1
            else:
                prog[args[2]] = 0
        elif op == 8:
            a0 = parse_arg(prog,args[0], parameter_modes[0])
            a1 = parse_arg(prog,args[1], parameter_modes[1])
            if a0 == a1:
                prog[args[2]] = 1
            else:
                prog[args[2]] = 0
        elif op == 99:
            status = 0
        else:
            status = -1

        return status,rtn


def run_prog_for_amp(prog, setting, signal):

    p = IntCode(prog)
    running = True
    given_setting = False

    while running:
        status = p.run_prog()
        if status == 3:
            if not given_setting:
                p.give_input(setting)
                given_setting = True
            else:
                p.give_input(signal)
        elif status == 0 or status == -1:
            running = False

    return p.get_output()


def check_sequence(prog, seq):
    prev_stage_power = 0
    for s in seq:
        prog_copy = copy.deepcopy(prog)
        prev_stage_power = run_prog_for_amp(prog_copy, s, prev_stage_power)

    return prev_stage_power


def find_max(prog):
    best_score = 0
    best_idx = []
    for it in itertools.permutations([0,1,2,3,4]):
        score = check_sequence(prog, it)
        if score > best_score:
            best_score = score
            best_idx = it

    return best_score, best_idx


def run_feedback_prog_for_all_amps(prog, seq):
    progs = []
    for s in seq:
        progs.append(IntCode(copy.copy(prog)))
        progs[-1].give_input(s)

    running = True
    prog_idx = 0
    next_signal = 0
    max_idx = 4
    while running:
        status = progs[prog_idx].run_prog()
        if status == 3:
            progs[prog_idx].give_input(next_signal)
        elif status == 4:
            next_signal = progs[prog_idx].get_output()
            prog_idx += 1
            if prog_idx > max_idx:
                prog_idx = 0
        elif status == 0 or status == -1:
            prog_idx += 1
            if prog_idx > max_idx:
                running = False

    return next_signal


def find_max_feedback(prog):
    best_score = 0
    best_idx = []
    for it in itertools.permutations([5,6,7,8,9]):
        score = run_feedback_prog_for_all_amps(prog, it)
        if score > best_score:
            best_score = score
            best_idx = it

    return best_score, best_idx
    


if __name__ == '__main__':

    with open('Day7/input.txt','r') as f:
        text = f.read()
        prog_str = text.split(',')
        prog = [int(x) for x in prog_str]
        print(find_max_feedback(prog))

