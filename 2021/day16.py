import sys
sys.path.append('.')
import aoc
import math
from aoc_utils.conversions import Binlist, hex_str_to_bin_list
from dataclasses import dataclass
from typing import Any

data_rows = aoc.get_input(16, sample=False).splitlines()

def version(packet: Binlist) -> int:
    return Binlist(packet[:3]).to_int()

def type_id(packet: Binlist) -> int:
    return Binlist(packet[3:6]).to_int()

def length_type_id(packet: Binlist) -> int:
    assert type_id(packet) != 4
    return int(packet[6])

def sub_packet_bit_length(packet: Binlist) -> int:
    assert length_type_id(packet) == 0
    return Binlist(packet[7:22]).to_int()

def sub_packet_num(packet: Binlist) -> int:
    assert length_type_id(packet) == 1
    return Binlist(packet[7:18]).to_int()

def sub_packet_contents(packet: Binlist) -> Binlist:
    if length_type_id(packet) == 0:
        return Binlist(packet[22:])
    else:
        return Binlist(packet[18:])

def decode_literal_value(packet: Binlist) -> tuple[int, int]:
    assert type_id(packet) == 4
    out = Binlist()
    found_stop = False
    index = 6
    while not found_stop:
        chunk = packet[index:index+5]
        prefix = chunk[0]
        out += chunk[1:]
        index += 5
        found_stop = not prefix
    return (out.to_int(), index)

@dataclass
class ParseInfo:
    version_sum: int
    data: Any
    end_index: int

def decode_and_sum_versions(packet: Binlist) -> ParseInfo:
    version_sum = version(packet)
    if type_id(packet) == 4:
        value, index = decode_literal_value(packet)
        # print(f"Literal value: {value}")
        return ParseInfo(version_sum, value, index)
    else:
        contents = sub_packet_contents(packet)
        bits_read = 0
        header_bits = 0
        data = []
        if length_type_id(packet) == 0:
            n_bits = sub_packet_bit_length(packet)
            # print(f"Bit operator packet: {n_bits}") 
            header_bits = 22
            loop_count = 0
            while bits_read < n_bits:
                sub_info = decode_and_sum_versions(Binlist(contents[bits_read:]))
                bits_read += sub_info.end_index
                version_sum += sub_info.version_sum
                data.append(sub_info.data)
                # print(f"Read bit loop {loop_count}: bits: {bits_read}, version_sum: {version_sum}, data: {data}")
                loop_count += 1
        else:
            n_packets = sub_packet_num(packet)
            # print(f"Num operator packet: {n_packets}")
            header_bits = 18
            for i in range(n_packets):
                sub_info = decode_and_sum_versions(Binlist(contents[bits_read:]))
                bits_read += sub_info.end_index
                version_sum += sub_info.version_sum
                data.append(sub_info.data)
                # print(f"Read num loop {i}: bits: {bits_read}, version_sum: {version_sum}, data: {data}")
            
        return ParseInfo(version_sum, data, bits_read + header_bits)



def part1():
    for row in data_rows:
        packet = hex_str_to_bin_list(row)
        # print(f"Raw: {str(packet)}\nVersion: {version(packet)}\nType_id: {type_id(packet)}\nVal: {decode_literal_value(packet)}")
        print("-----------")
        print(decode_and_sum_versions(packet))
# part1()

def do_operation(id, data):
    # print(f"Performing operation {id} with data: {data}")
    if id == 0:
        return sum(data)
    elif id == 1:
        return math.prod(data)
    elif id == 2:
        return min(data)
    elif id == 3:
        return max(data)
    elif id == 5:
        return int(data[0] > data[1])
    elif id == 6:
        return int(data[0] < data[1])
    elif id == 7:
        return int(data[0] == data[1])

def decode(packet: Binlist) -> ParseInfo:
    if type_id(packet) == 4:
        value, index = decode_literal_value(packet)
        # print(f"Literal value: {value}")
        return ParseInfo(0, value, index)
    else:
        contents = sub_packet_contents(packet)
        bits_read = 0
        header_bits = 0
        data = []
        if length_type_id(packet) == 0:
            n_bits = sub_packet_bit_length(packet)
            # print(f"Bit operator packet: {n_bits}") 
            header_bits = 22
            loop_count = 0
            while bits_read < n_bits:
                sub_info = decode(Binlist(contents[bits_read:]))
                bits_read += sub_info.end_index
                data.append(sub_info.data)
                # print(f"Read bit loop {loop_count}: bits: {bits_read}, data: {data}")
                loop_count += 1
        else:
            n_packets = sub_packet_num(packet)
            # print(f"Num operator packet: {n_packets}")
            header_bits = 18
            for i in range(n_packets):
                sub_info = decode(Binlist(contents[bits_read:]))
                bits_read += sub_info.end_index
                data.append(sub_info.data)
                # print(f"Read num loop {i}: bits: {bits_read}, data: {data}")

        data = do_operation(type_id(packet), data)

        return ParseInfo(0, data, bits_read + header_bits)

def part2():
    for row in data_rows:
        packet = hex_str_to_bin_list(row)
        print("-----------")
        print(decode(packet))
part2()