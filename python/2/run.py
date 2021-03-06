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
        with open("python/2/input.txt", "r") as f:
            raw_input  = f.read()
raw_input = raw_input.strip()

input = (
    Input(raw_input)
        # .all()
        # .ints()
        # .int_tokens()
        # .tokens()
        # .lines()
        .line_tokens()
        # .line_tokens(sep = "\n", line_sep = "\n\n")
)

def part1(input):
    x, y = 0, 0
    for (d, n) in input:
        if d == 'forward':
            x += int(n)
        elif d == 'down':
            y += int(n)
        elif d == 'up':
            y -= int(n)
    return x * y

def part2(input):
    x, y, aim = 0, 0, 0
    for (d, n) in input:
        if d == 'forward':
            x += int(n)
            y += aim * int(n)
        elif d == 'down':
            aim += int(n)
        elif d == 'up':
            aim -= int(n)
    return x * y

def solve(input):
    return part1(input), part2(input)

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(2, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(2, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")