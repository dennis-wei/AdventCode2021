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
        with open("python/5/input.txt", "r") as f:
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

def is_vert(r):
    return r[0][0] == r[1][0]

def is_hor(r):
    return r[0][1] == r[1][1]

def is_hor_vert(r):
    return is_hor(r) or is_vert(r)

def make_grid1(input):
    split = [r.split(" -> ") for r in input]
    as_nums = [[get_all_nums(t) for t in r] for r in split]
    ho_vert = filter(lambda x: is_hor_vert(x), as_nums)

    grid = defaultdict(int)

    for r in ho_vert:
        ((x1, y1), (x2, y2)) = r
        if x1 == x2:
            miny, maxy = min(y1, y2), max(y1, y2)
            for i in range(miny, maxy + 1):
                grid[(x1, i)] += 1
        if y1 == y2:
            minx, maxx = min(x1, x2), max(x1, x2)
            for i in range(minx, maxx + 1):
                grid[(i, y1)] += 1
    
    return grid

def make_grid2(input):
    split = [r.split(" -> ") for r in input]
    as_nums = [[get_all_nums(t) for t in r] for r in split]

    grid = defaultdict(int)

    for r in as_nums:
        ((x1, y1), (x2, y2)) = r
        if x1 == x2:
            miny, maxy = min(y1, y2), max(y1, y2)
            for i in range(miny, maxy + 1):
                grid[(x1, i)] += 1
        elif y1 == y2:
            minx, maxx = min(x1, x2), max(x1, x2)
            for i in range(minx, maxx + 1):
                grid[(i, y1)] += 1
        else:
            if x2 > x1:
                xdiff = 1
            else:
                xdiff = -1
            if y2 > y1:
                ydiff = 1
            else:
                ydiff = -1
            
            curr = (x1, y1)
            for i in range(abs(x2 - x1) + 1):
                grid[curr] += 1
                curr = (curr[0] + xdiff, curr[1] + ydiff)
    
    return grid

def solve(input):
    grid1 = make_grid1(input)
    grid2 = make_grid2(input)
    return len([e for e in grid1.values() if e > 1]), len([e for e in grid2.values() if e > 1])

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(5, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(5, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")