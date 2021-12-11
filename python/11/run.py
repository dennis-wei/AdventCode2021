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
            with open("11/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/11/input.txt", "r") as f:
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

def recur_flash(grid, will_flash, flashed):
    for p in will_flash:
        (x, y) = p
        for neighbor, n in grid.get_adjacent(x, y, diagonal=True).items():
            if neighbor not in flashed:
                grid.grid[neighbor] = n + 1

    for p in will_flash:
        grid.grid[p] = 0
        flashed.add(p)
    
    # grid.print_grid({10: "A", 11: "B"})

    will_flash_next = []
    for p, v in grid.items():
        if v > 9 and p not in flashed:
            will_flash_next.append(p)

    if len(will_flash_next) > 0:
        recur_flash(grid, will_flash_next, flashed)
    
    return len(flashed)

def simul(grid):
    will_flash = []
    for p, v in grid.items():
        grid.grid[p] = v + 1
    
    return recur_flash(grid, will_flash, set())

def solve(input):
    as_nums = [[int(c) for c in line] for line in input]
    grid = Grid(as_nums)

    p1_acc = 0
    iter = 0
    while True:
        iter += 1
        num_flashed = simul(grid)
        if iter <= 100:
            p1_acc += num_flashed
        if num_flashed == len(grid.grid):
            break

    return p1_acc, iter

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(11, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(11, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")