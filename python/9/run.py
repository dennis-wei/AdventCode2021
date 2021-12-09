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
        try:
            with open("9/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/9/input.txt", "r") as f:
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

def recurse(grid, point, n, traversed, acc):
    if point in traversed:
        return

    (x, y) = point
    traversed.add(point)
    acc.append(point)
    for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        padj = (x + dx, y + dy)
        if padj in grid and grid[padj] > n and grid[padj] != 9:
            recurse(grid, padj, grid[padj], traversed, acc)

def solve(input):
    grid = {}
    for i, row in enumerate(input):
        for j, c in enumerate(row):
            grid[(i, j)] = int(c)
    
    mins = 0
    min_points = []
    for (x, y), n in grid.items():
        is_min = True
        for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            padj = (x + dx, y + dy)
            if padj in grid and grid[padj] <= n:
                is_min = False
        if is_min:
            min_points.append((x, y))
            mins += n + 1
    
    basins = {}
    basin_sizes = {}
    for (x, y) in min_points:
        acc = []
        traversed = set()
        recurse(grid, (x, y), grid[(x, y)], traversed, acc)

        basin_sizes[(x, y)] = len(acc)
        basins[(x, y)] = acc
    
    top = sorted(basin_sizes.values(), reverse = True)[:3]
    p2 = top[0] * top[1] * top[2]

    return mins, p2

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(9, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(9, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")