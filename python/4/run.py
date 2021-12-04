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
        with open("python/4/input.txt", "r") as f:
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

def make_grid(g):
    print(g)
    grid = {}
    inv_grid = {}
    s = 0
    for i, row in enumerate(g):
        print(row)
        for j, n in enumerate(row.split()):
            grid[(i, j)] = int(n)
            inv_grid[int(n)] = (i, j)
            s += int(n)
    return grid, inv_grid, s, [], {"row": defaultdict(int), "col": defaultdict(int)}

def won(marked):
    return 

def mark_and_ret_win(gdata, c):
    grid, inv_grid, s, called, mgrid = gdata
    if c in inv_grid:
        (i, j) = inv_grid[c]
        called.append(c)
        mgrid["row"][i] += 1
        mgrid["col"][j] += 1
    if 5 in mgrid["row"].values() or 5 in mgrid["col"].values():
        return c * (s - sum(called))
    return None

def solve1(input):
    calls = [int(n) for n in input[0][0].split(",")]
    grids = [make_grid(i) for i in input[1:]]
    for c in calls:
        res = [mark_and_ret_win(g, c) for g in grids]
        for e in res:
            if e:
                return e

def solve2(input):
    calls = [int(n) for n in input[0][0].split(",")]
    grids = [make_grid(i) for i in input[1:]]
    won_turn = {}
    for i, c in enumerate(calls):
        res = [mark_and_ret_win(g, c) for g in grids]
        for j, e in enumerate(res):
            if e and j not in won_turn:
                won_turn[j] = (i, e)
    
    last = max(won_turn.items(), key = lambda x: x[1][0])
    return last[1][1]

def solve(input):
    return solve1(input), solve2(input)

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(4, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(4, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")