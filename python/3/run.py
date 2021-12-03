import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque
from util.helpers import split_newline, space_split, int_parsed_list, list_of_ints, get_all_nums, submit, Input
from math import floor, ceil
from functools import reduce
from copy import deepcopy

parser = argparse.ArgumentParser()
parser.add_argument("--from-std-in", action='store_true', default=False)
args = parser.parse_args()
if args.from_std_in:
    raw_input = clipboard.paste()
else:
    try:
        with open("input.txt", "r") as f:
            raw_input = f.read()
    except:
        with open("python/3/input.txt", "r") as f:
            raw_input  = f.read()
raw_input = raw_input.strip()

input = (
    Input(raw_input)
        # .all()
        # .ints()
        # .int_tokens()
        # .tokens()
        .lines()
        # .line_tokens()
        # .line_tokens(sep = "\n", line_sep = "\n\n")
)

def to_int(bin_arr):
    bin_str = "".join(str(n) for n in bin_arr)
    return int(bin_str, 2)

def do_ogr_filter(input, index):
    acc = 0
    for r in input:
        if r[index] == "1":
            acc += 1
        else:
            acc -= 1
    
    if acc >= 0:
        return [r for r in input if r[index] == "1"]
    else:
        return [r for r in input if r[index] == "0"]

def do_csr_filter(input, index):
    acc = 0
    for r in input:
        if r[index] == "1":
            acc += 1
        else:
            acc -= 1
    
    if acc >= 0:
        return [r for r in input if r[index] == "0"]
    else:
        return [r for r in input if r[index] == "1"]

def part1(input):
    zipped = zip(*input)
    summed = [sum([int(n) for n in r]) for r in zipped]
    transformed = [1 if n > len(input) / 2 else 0 for n in summed]
    inverse = [0 if n > len(input) / 2 else 1 for n in summed]
    return to_int(transformed) * to_int(inverse)

def part2(input):
    ogr_index = 0
    ogr_filtered = input
    while len(ogr_filtered) > 1:
        ogr_filtered = do_ogr_filter(ogr_filtered, ogr_index)
        ogr_index += 1

    csr_index = 0
    csr_filtered = input
    while len(csr_filtered) > 1:
        csr_filtered = do_csr_filter(csr_filtered, csr_index)
        csr_index += 1
    
    int(ogr_filtered[0], 2) * int(csr_filtered[0], 2)

def solve(input):
    return part1(input), part2(input)

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(3, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(3, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")