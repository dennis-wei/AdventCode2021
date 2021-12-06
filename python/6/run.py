import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations
from collections import defaultdict, Counter, deque, OrderedDict
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
        with open("python/6/input.txt", "r") as f:
            raw_input  = f.read()
raw_input = raw_input.strip()

input = (
    Input(raw_input)
        # .all()
        # .ints()
        .int_tokens()
        # .tokens()
        # .lines()
        # .line_tokens()
        # .line_tokens(sep = "\n", line_sep = "\n\n")
)

def solve(input, target=80):
    print()
    m = OrderedDict()
    m[1] = {
        0: [8, 6],
        1: [0],
        2: [1],
        3: [2],
        4: [3],
        5: [4],
        6: [5],
        7: [6],
        8: [7],
    }

    curr = 1
    while curr < target:
        max_idx = -1
        while curr + list(m.keys())[max_idx] > target:
            max_idx -= 1
        to_add = list(m.keys())[max_idx]
        new_curr = curr + to_add
        new_entry = {}
        for i in range(9):
            # Can't actually flat map elements after this, so just get count
            if new_curr == 256:
                new_entry[i] = sum(len(m[to_add][x]) for x in m[curr][i])
                continue
            mapped = map(lambda x: m[to_add][x], m[curr][i])
            flattened = [item for sublist in mapped for item in sublist]
            new_entry[i] = list(flattened)
        
        m[new_curr] = new_entry
        curr = new_curr
    
    if target == 80:
        res = reduce(lambda x, y: x + len(y), [m[target][r] for r in input[0]], 0)
    elif target == 256:
        res = reduce(lambda x, y: x + y, [m[target][r] for r in input[0]], 0)
    return res

start = time.time()
p1 = solve(input, 80)
p2 = solve(input, 256)
answer1, answer2 = p1, p2

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(6, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(6, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")