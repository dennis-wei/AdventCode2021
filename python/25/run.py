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
            with open("25/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/25/input.txt", "r") as f:
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

def make_grid(input):
    grid = {}
    height = len(input)
    width = len(input[0])
    for j, row in enumerate(input):
        for i, c in enumerate(row):
            grid[(i, j)] = c
    return grid, (width, height)

def iter(grid, dims):
    moved = False
    width, height = dims
    right_updated_grid = {}
    right_skip = set()
    for j in range(height):
        for i in range(width):
            if (i, j) in right_skip:
                continue
            if grid[(i, j)] == ">":
                if i + 1 == width:
                    neighbor = (0, j)
                else:
                    neighbor = (i + 1, j)
                if grid[neighbor] == ".":
                    right_updated_grid[(i, j)] = "."
                    right_updated_grid[neighbor] = ">"
                    right_skip.add(neighbor)
                    moved = True
                else:
                    right_updated_grid[(i, j)] = ">"
            else:
                right_updated_grid[(i, j)] = grid[(i, j)]
    
    # print_grid(right_updated_grid, dims)
    
    down_updated_grid = {}
    down_skip = set()
    for j in range(height):
        for i in range(width):
            if (i, j) in down_skip:
                continue
            if right_updated_grid[(i, j)] == "v":
                if j + 1 == height:
                    neighbor = (i, 0)
                else:
                    neighbor = (i, j + 1)
                if right_updated_grid[neighbor] == ".":
                    down_updated_grid[(i, j)] = "."
                    down_updated_grid[neighbor] = "v"
                    down_skip.add(neighbor)
                    moved = True
                else:
                    down_updated_grid[(i, j)] = "v"
            else:
                down_updated_grid[(i, j)] = right_updated_grid[(i, j)]
    return not moved, down_updated_grid

def print_grid(grid, dims):
    width, height = dims
    for j in range(height):
        for i in range(width):
            print(grid[(i, j)], end="")
        print()
    print()

def solve(input, verbose = False):
    grid, dims = make_grid(input)
    static = False
    
    if verbose:
        print_grid(grid, dims)

    updated_grid = deepcopy(grid)
    iters = 0
    while not static:
        iters += 1
        static, updated_grid = iter(updated_grid, dims)
        if verbose:
            print(f"after {iters} steps")
            print_grid(updated_grid, dims)
    
    return iters, None

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(25, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(25, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")