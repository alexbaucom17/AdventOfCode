
def do_op(prog, op, args, parameter_modes):
    #print("Running op {} with modes {} and args {}".format(op, args, parameter_modes))

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
        prog[args[0]] = int(input('Input: '))
    elif op == 4:
        a0 = parse_arg(prog,args[0], parameter_modes[0])
        print(a0)
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

def run_prog(prog):
    idx = 0

    while True:
        op = prog[idx]
        opcode, modes = parse_opcode(op)
        n_args = num_args_for_op(opcode)
        args = prog[idx+1:idx+1+n_args]
        status, rtn = do_op(prog, opcode, args, modes)
        if status == 0:
            break
        elif status == -1:
            print('ERROR!')
        elif status == 2:
            idx = rtn
        else:
            idx += n_args+1


if __name__ == '__main__':

    with open('Day5/input.txt','r') as f:
        text = f.read()
        prog_str = text.split(',')
        prog = [int(x) for x in prog_str]
        run_prog(prog)


        

