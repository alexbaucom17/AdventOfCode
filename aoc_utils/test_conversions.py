import sys
sys.path.append('.')
from aoc_utils.conversions import Binlist, hex_str_to_bin_list

def test_binlist():
    test_data = [
            ([0,0,0,1], 1, "0001"),
            ([1,1,0,0,0,1,0,1], 197, "11000101"),
            ([5,1,0,2], 13, "1101"),
            ([True, False, True, False], 10, "1010"),
            ]
    for input, dec, string in test_data:
        b = Binlist(input)
        assert dec == b.to_int()
        assert string == str(b)


def test_hex_str_to_bin_list():
    test_data = [
        ("D2FE28", "110100101111111000101000"),
        ("38006F45291200", "00111000000000000110111101000101001010010001001000000000"),
        ("EE00D40C823060", "11101110000000001101010000001100100000100011000001100000")
    ]
    for hex_str, bin_str in test_data:
        b = hex_str_to_bin_list(hex_str)
        assert str(b) == bin_str