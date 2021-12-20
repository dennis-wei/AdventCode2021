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
            with open("20/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/20/input.txt", "r") as f:
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

def print_grid(grid):
    min_x = min(t[0] for t in grid)
    max_x = max(t[0] for t in grid)
    min_y = min(t[1] for t in grid)
    max_y = max(t[1] for t in grid)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            print(grid[(x, y)], end="")
        print()

def get_enhanced(grid, algo, i, j, iter):
    acc = ""
    if iter % 2 == 1:
        default = "."
    else:
        default = "#"
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            acc += grid.get((i + dx, j + dy), default)
    
    # print(i, j, acc)
    
    in_bin = ["1" if c == "#" else "0" for c in acc]
    return algo[int("".join(in_bin), 2)]

def populate_neighbors(grid, i, j, parity, amount):
    if parity % 2 == 1:
        to_pop = "."
    else:
        to_pop = "#"
    for dx in range(-amount, amount + 1):
        for dy in range(-amount, amount + 1):
            coord = (i + dx, j + dy)
            if not coord in grid:
                grid[coord] = to_pop

def pad(grid, iter, amount=2):
    for i, j in set(grid.keys()):
        populate_neighbors(grid, i, j, iter, amount)

def simulate(grid, algo, iter):
    # print("start")
    # print_grid(grid)
    updated_grid = defaultdict(lambda: ".")
    pad(grid, iter)
    # print("post-pad")
    # print_grid(grid)
    for i, j in grid.keys():
        updated_grid[(i, j)] = get_enhanced(grid, algo, i, j, iter)
    # print("end")
    # print_grid(updated_grid)
    return updated_grid

def solve(input, num_iters):
    raw_algo, raw_image = input
    algo = "".join(raw_algo)

    grid = defaultdict(lambda x: ".")
    for i, row in enumerate(raw_image):
        for j, c in enumerate(row):
            grid[(i, j)] = c
    
    for i in range(1, num_iters + 1):
        print(i)
        grid = simulate(grid, algo, i)
    return sum(1 if v == "#" else 0 for v in grid.values())

start = time.time()
answer1 = solve(input, 2)
answer2 = solve(input, 50)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(20, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(20, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")