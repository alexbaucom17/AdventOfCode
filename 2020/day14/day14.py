def load_data(filename):
    with open(filename) as f:
        data = [parse_data(line.rstrip()) for line in f]
        return data

def parse_data(data):
    inst, arg = data.split('=')
    if inst.startswith("mask"):
        m = arg.strip()
        ones_mask = ''.join(['1' if c == '1' else '0' for c in m])
        zero_mask = ''.join(['0' if c == '0' else '1' for c in m])
        x_mask = ''.join(['0' if c == 'X' else '1' for c in m])
        return ("mask", x_mask, ones_mask, zero_mask)
    elif inst.startswith("mem"):
        return ("mem", int(inst[inst.find("[")+1:inst.rfind("]")]), int(arg.strip()))
    else:
        raise ValueError("Unknown data format: {}".format(data))

def apply_mask(masks, num):
    affected_mask = int(masks[0], 2)
    ones_mask = int(masks[1], 2)
    zero_mask = int(masks[2], 2)
    # print('ones_mask: {0:b}'.format(ones_mask))
    # print('zero_mask: {0:b}'.format(zero_mask))
    # print('Num: {0:b}'.format(num))

    # Num with all affected bits zeroed
    num = num & (~ affected_mask)
    # print('Num: {0:b}'.format(num))

    # Add back ones
    num = num | ones_mask
    # print('Num: {0:b}'.format(num))

    return num

def perform_instructions(inst, data_map):
    cur_mask = ()
    for i in inst:
        if i[0] == 'mask':
            cur_mask = tuple(i[1:])
        elif i[0] == 'mem':
            data_map[i[1]] = apply_mask(cur_mask, i[2])
        
    return data_map


def apply_memory_mask(masks, addr):

    # print('addr: {0:b}, {0:d}'.format(addr,addr))
    # Apply ones
    ones_mask = int(masks[1], 2)
    addr = addr | ones_mask
    # print('addr: {0:b}, {0:d}'.format(addr,addr))

    # zero Xs
    x_mask = masks[0]
    addr = addr & int(x_mask,2)
    # print('addr: {0:b}, {0:d}'.format(addr,addr))

    # Get x positions
    xs = [pos for pos, char in enumerate(reversed(x_mask)) if char == '0']
    # print(xs)

    # initialize addrs
    addrs = []
    addrs.append(addr)
    for x in xs:
        new_addrs = []
        for a in addrs:
            m = 1 << x
            new_addrs.append(a & (~m))
            new_addrs.append(a | m)
        addrs = new_addrs

    return addrs

def perform_instructions_v2(inst, data_map):
    cur_mask = ()
    for i in inst:
        if i[0] == 'mask':
            cur_mask = tuple(i[1:])
        elif i[0] == 'mem':
            addrs = apply_memory_mask(cur_mask, i[1])
            for a in addrs:
                data_map[a] = i[2]
        
    return data_map



if __name__ == '__main__':

    sample_data = load_data("day14/sample_input.txt")
    sample_data2 = load_data("day14/sample_input2.txt")
    data = load_data("day14/input.txt") 

    #output = perform_instructions(data, {})
    
    # print(sample_data2)
    # addrs = apply_memory_mask(sample_data2[2][1:], sample_data2[3][1])
    # for a in addrs:
    #     print('addr: {0:b}, {0:d}'.format(a,a))

    output = perform_instructions_v2(data, {})
    # print(output)
    s = 0
    for v in output.values():
        s += v
    print(s)