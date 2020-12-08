import copy

def do_op(prog, idx):
    op = prog[idx]

    if op == 1:
        idx_1 = prog[idx+1]
        idx_2 = prog[idx+2]
        idx_store = prog[idx+3]
        prog[idx_store] = prog[idx_1] + prog[idx_2]
        return 1
    elif op == 2:
        idx_1 = prog[idx+1]
        idx_2 = prog[idx+2]
        idx_store = prog[idx+3]
        prog[idx_store] = prog[idx_1] * prog[idx_2]
        return 1
    elif op == 99:
        return 0
    else:
        return -1

def run_prog(prog):
    op_idx = 0
    status = 1
    while status == 1:
        status = do_op(prog, op_idx)
        op_idx += 4

def init_and_run_prog(prog, noun, verb):
    prog[1] = noun
    prog[2] = verb
    run_prog(prog)
    return prog[0]

def prog_search(target, default_prog, min, max):
    for noun in range(min, max+1):
        for verb in range(min, max+1):
            print("Checking ({},{})".format(noun, verb))
            prog = copy.deepcopy(default_prog)
            result = init_and_run_prog(prog, noun, verb)
            if result == target:
                return 100*noun + verb      
    return -1


if __name__ == '__main__':
    #test_prog = [1,1,1,4,99,5,6,0,99]
    #run_prog(test_prog)

    with open('Day2/input.txt','r') as f:
        text = f.read()
        prog_str = text.split(',')
        default_prog = [int(x) for x in prog_str]
        result = prog_search(19690720, default_prog, 0, 99)
        print(result)


    