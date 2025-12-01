import sys
sys.path.append('.')
import aoc
import math
from aoc_utils.conversions import str_to_binlist, Binlist
import numpy as np

data_rows = aoc.get_input(20, sample=False, index=0).splitlines()

def parse():
    algo = str_to_binlist(data_rows[0], '#', '.')
    # algo[0] = False
    image = []
    for row in data_rows[2:]:
        image.append(str_to_binlist(row, '#', '.'))
    return algo, np.asarray(image, dtype=bool)

def safe_get(image, default, rowstart, rowend, colstart, colend):
    data = []
    for i in range(rowstart, rowend+1):
        for j in range(colstart, colend+1):
            if i < 0 or i >= image.shape[0] or j < 0 or j >= image.shape[1]:
                data.append(default)
            else:
                data.append(image[i,j])
    return data

def enhance(image, external_default, algo, padding):
    padded_image = np.pad(image, padding, constant_values=external_default)
    n_rows, n_cols = padded_image.shape
    out_image = np.zeros_like(padded_image)
    for i in range(n_rows):
        for j in range(n_cols):
            # subset = padded_image[i-1:i+2,j-1:j+2]
            # subset_flattened = subset.flatten()
            # # print(f"Index: ({i},{j})")
            # # print_image(subset)
            # # print(subset_flattened)
            subset_flattened = safe_get(padded_image, external_default, i-1, i+1, j-1, j+1)
            num = Binlist(list(subset_flattened)).to_int()
            out_image[i,j] = algo[num]
    # if padding > 1:
    #     out_image = out_image[1:out_image.shape[0]-1, 1:out_image.shape[1]-1]
    external_default = algo[Binlist([external_default]*9).to_int()]
    return out_image, external_default

def print_image(image):
    for i in range(image.shape[0]):
        line = ""
        for j in range(image.shape[1]):
            char = '#' if image[i,j] else '.'
            line += char
        print(line)
    print('---------------')


def part1():
    algo, image = parse()
    default = False
    # print(len(algo))
    # print(image.shape)
    # print_image(image)
    # print(np.sum(np.sum(image)))
    for i in range(50):
        # padding = 500 if i == 0 else 0
        image, default = enhance(image, default, algo, padding=2)
        # print_image(image)
        print(f"{i+1}: {np.sum(np.sum(image))}, {default}")
    

part1()

