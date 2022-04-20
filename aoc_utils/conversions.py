import math
from typing import Union

class Binlist(list):
    def __init__(self, data: Union[list[bool], list[int]] = []):
        super().__init__([bool(x) for x in data])

    def to_int(self):
        num = 0
        power = 0
        for i in range(len(self), 0, -1):
            num += math.pow(2, power) * self[i-1]
            power += 1
        return int(num)

    def __str__(self):
        out = ""
        for d in self:
            out += str(int(d))
        return out

def str_to_binlist(s: str, true_char: str, false_char: str):
    data = []
    for c in s:
        if c not in [true_char, false_char]:
            raise ValueError(f"Tried to parse char {c} but it is not in set ({true_char}, {false_char})")
        data.append(bool(c==true_char))
    return Binlist(data)

hex_map = {
    '0':[0,0,0,0],
    '1':[0,0,0,1],
    '2':[0,0,1,0],
    '3':[0,0,1,1],
    '4':[0,1,0,0],
    '5':[0,1,0,1],
    '6':[0,1,1,0],
    '7':[0,1,1,1],
    '8':[1,0,0,0],
    '9':[1,0,0,1],
    'A':[1,0,1,0],
    'B':[1,0,1,1],
    'C':[1,1,0,0],
    'D':[1,1,0,1],
    'E':[1,1,1,0],
    'F':[1,1,1,1],
}
def hex_str_to_bin_list(hex: str) -> Binlist:
    outlist = []
    for c in hex.strip():
        outlist += hex_map[c]
    return Binlist(outlist)

