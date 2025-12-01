import sys
sys.path.append('.')
import aoc
import math
from joblib import Parallel, delayed
import time

data_rows = aoc.get_input(24, sample=False, index=2).splitlines()

class ALUGen:

    def __init__(self, gen_debug: bool = False):
        self.gen_str = "import math\ndef gen_fn(input_arr: list[int]):\n"
        self.gen_str += "\tw=0\n\tx=0\n\ty=0\n\tz=0\n"

        self.input_count = 0
        self.gen_debug = gen_debug

        self.gen_block_str = ""

        if self.gen_debug:
            self.gen_str += self._gen_line("print(input_arr)")

    def write(self):
        if self.gen_debug:
            self.gen_st += self._gen_line("print(f'Before return:       w={w} x={x} y={y} z={z}')")
        self.gen_str += self._gen_line("return z")
        self.gen_str += self.gen_block_str
        self.gen_str += self._gen_block_end()

        name = "AdventofCode2021/day24_gen.py"
        with open(name, "w") as f:
            f.write(self.gen_str)
        print(f"Generated file at {name}")

    def _gen_line(self, line):
        return f"\t{line}\n"

    def gen_op(self, op: str):
        parts = op.split()
        inst = parts[0]
        args = parts[1:]
        if inst == "inp":
            self.gen_str += self._gen_inp_main(args)
            self.gen_block_str += self._gen_inp_block( args)
            self.input_count += 1
        else:
            self.gen_str += self._gen_op(inst, args)
            self.gen_block_str += self._gen_op(inst, args)

    def _gen_inp_main(self, args):
        s = ""
        if self.gen_debug:
            s += self._gen_line("print(f'Before input {0} ({{input_arr[{1}]}}): w={{w}} x={{x}} y={{y}} z={{z}}')".format(self.input_count, self.input_count))
        s += self._gen_line(f"{args[0]}=input_arr[{self.input_count}]")
        return s

    def _gen_inp_block(self, args):
        s = ""
        if self.input_count > 0:
            s += self._gen_block_end()
        s += f"\ndef block{self.input_count}(in_val, in_z):\n"
        s += "\tx=0\n\ty=0\n\tz=in_z\n"
        s += self._gen_line(f"{args[0]}=in_val")
        return s

    def _gen_block_end(self):
        s = ""
        if self.gen_debug:
            s += self._gen_line("print(f'Before return {0} ({{in_val}}): w={{w}} x={{x}} y={{y}} z={{z}}')".format(self.input_count, self.input_count))
        s += self._gen_line(f"return z")
        return s

    def _gen_op(self, inst, args):           
        if inst == "add":
            return self._gen_line(f"{args[0]}={args[0]}+{args[1]}")
        elif inst == "mul":
            if args[1] == '0':
                return self._gen_line(f"{args[0]}=0 # Was multiply by 0")
            else:
                return self._gen_line(f"{args[0]}={args[0]}*{args[1]}")
        elif inst == "div":
            if args[1] == '1':
                return self._gen_line(f"# Skipped {args[0]} div by 1")
            else:
                return self._gen_line(f"{args[0]}=math.floor({args[0]}/{args[1]})")
        elif inst == "mod":
            return self._gen_line(f"{args[0]}={args[0]}%{args[1]}")
        elif inst == "eql":
            return self._gen_line(f"{args[0]}=int({args[0]}=={args[1]})")
        else:
            raise ValueError(f"Unsupported instruction type {inst}")
        
def number_gen(nums, max_count):
    count = 0
    yield nums
    while count < max_count:
        for i in range(13, -1, -1):
            nums[i] -= 1
            if nums[i] > 0:
                break
            else:
                nums[i] = 9
        count += 1
        yield nums

def join_num(num):
    s = ""
    for n in num:
        s += str(n)
    return s

def split_num(num):
    return [int(c) for c in str(num)]

def run_gen():
    gen = ALUGen(gen_debug=False)
    for line in data_rows:
        gen.gen_op(line)
    gen.write()
run_gen()
from day24_gen import *

def run_block(i, in_val, z):
    if i == 0:
        return block0(in_val, z)
    elif i == 1:
        return block1(in_val, z)
    elif i == 2:
        return block2(in_val, z)
    elif i == 3:
        return block3(in_val, z)
    elif i == 4:
        return block4(in_val, z)
    elif i == 5:
        return block5(in_val, z)
    elif i == 6:
        return block6(in_val, z)
    elif i == 7:
        return block7(in_val, z)
    elif i == 8:
        return block8(in_val, z)
    elif i == 9:
        return block9(in_val, z)
    elif i == 10:
        return block10(in_val, z)
    elif i == 11:
        return block11(in_val, z)
    elif i == 12:
        return block12(in_val, z)
    elif i == 13:
        return block13(in_val, z)

def run_all_blocks(input_arr):
    z = 0
    for i in range(14):
        z = run_block(i, input_arr[i], z)
    return z

def testing():
    n = 13579246899999
    nums = [int(c) for c in str(n)]
    for i in range(10):
        nums[0] = i
        gen_fn(nums)
# testing()

def test_blocks():
    z = 24
    z = run_block(12, 9, z)
    print(z)
    z = run_block(13, 9, z)
    print(z)
# test_blocks()

def test_block_math():
    n = 99999999999959
    nums = split_num(n)
    print(f"Blocks: {run_all_blocks(nums)}, Full: {gen_fn(nums)}")
# test_block_math()

def block_search_helper(block_num, in_z, valid_end_zs):
    results = []
    for in_val in [1,2,3,4,5,6,7,8,9]:
        end_z = run_block(block_num, in_val, in_z)
        # print(f"Block{block_num}(in_val={in_val}, in_z={in_z}) = {end_z}")
        if end_z in valid_end_zs:
            results.append((in_val, in_z, end_z))
    return results

def flatten_results(res):
    out = []
    for r in res:
        if len(r) > 0:
            out += r
    return out

def block_search_par(block_num, max_count, valid_end_zs, parallel):
    res = parallel(delayed(block_search_helper)(block_num, in_z, valid_end_zs) for in_z in range(1, max_count))
    return flatten_results(res)

def block_search(block_num, max_count, valid_end_zs):
    res = []
    for in_z in range(1, max_count):
        res.append(block_search_helper(block_num, in_z, valid_end_zs))
    return flatten_results(res)

def backwards_search(max_count):
    seqs = {0: []}
    with Parallel(n_jobs=16) as parallel:
        for i in range(13, 0, -1):
            count = max_count
            if i > 11:
                count = max_count / 10
            results = block_search_par(i, max_count, seqs.keys(), parallel)
            # results = block_search(i, max_count, seqs.keys())
            new_seqs = {}
            for r in results:
                in_val, in_z, end_z = r
                if in_z in new_seqs:
                    s1 = [in_val] + seqs[end_z]
                    s2 = new_seqs[in_z]
                    # print(f'Checking {s1} vs {s2} for in_z {in_z}')
                    if int(join_num(s1)) < int(join_num(s2)):
                        new_seqs[in_z] = s1
                else:
                    new_seqs[in_z] = [in_val] + seqs[end_z]
            seqs = new_seqs
            print(f"Results for block{i}: Results - {len(results)}, Sequence map: {len(seqs)}")

    last_results = block_search_helper(0, 0, seqs.keys())
    all_nums = []
    for r in last_results:
        in_val, in_z, end_z = r
        num = [in_val] + seqs[end_z]
        n = int(join_num(num))
        all_nums.append(n)
    print(all_nums)

    best_num = 9999999999999999999
    for n in all_nums:
        if n < best_num:
            best_num = n
    print(best_num)


def part1():
    max_count = 1000000
    backwards_search(max_count)
part1()


# import cProfile
# pr = cProfile.Profile()
# pr.enable()
# pr.run('part1()')
# pr.disable()
# import pstats
# p = pstats.Stats(pr)
# p.sort_stats(pstats.SortKey.TIME)
# p.print_stats()

