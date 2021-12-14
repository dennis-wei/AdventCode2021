import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque
from util.helpers import split_newline, space_split, int_parsed_list, list_of_ints, get_all_nums, submit, Input, Grid
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
        try:
            with open("14/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/14/input.txt", "r") as f:
                raw_input  = f.read()
raw_input = raw_input.strip()

input = (
    Input(raw_input)
        # .all()
        # .ints()
        # .int_tokens()
        # .tokens()
        # .lines()
        # .line_tokens()
        .line_tokens(sep = "\n", line_sep = "\n\n")
)

def solve(input, iters):
    [start, raw_instructions] = input
    starting_code = start[0]

    pair_map = defaultdict(int)
    for t in zip(starting_code, starting_code[1:]):
        pair_map[t[0] + t[1]] += 1

    instructions = {}
    for r in raw_instructions:
        p, c = r.split(" -> ")
        instructions[p] = (p[0] + c, c + p[1])
    
    for i in range(iters):
        newmap = defaultdict(int)
        for k, v in pair_map.items():
            t1, t2 = instructions[k]
            newmap[t1] += v
            newmap[t2] += v
        pair_map = newmap
    
    char_counts = defaultdict(int)
    for k, v in pair_map.items():
        char_counts[k[0]] += v
    char_counts[starting_code[-1]] += 1
    
    most_common = max(char_counts.items(), key=lambda x: x[1])[1]
    least_common = min(char_counts.items(), key=lambda x: x[1])[1]

    return most_common - least_common

start = time.time()
answer1 = solve(input, 10)
answer2 = solve(input, 40)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(14, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(14, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")