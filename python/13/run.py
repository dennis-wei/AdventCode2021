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
            with open("13/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/13/input.txt", "r") as f:
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

def process_fold(f, grid):
    print("applying fold: ", f)
    axis, axis_n = f
    if axis == "x":
        curr_offset = 1
        min_y = min(y for x, y in grid)
        max_y = max(y for x, y in grid)
        while ((axis_n + curr_offset, min_y) in grid):
            for y in range(min_y, max_y + 1):
                existing = grid.get((axis_n - curr_offset, y), ".")
                updated = grid.get((axis_n + curr_offset, y), ".")

                if existing == "." and updated == ".":
                    new = "."
                else:
                    new = "#"
                
                grid[(axis_n - curr_offset, y)] = new
                grid.pop((axis_n + curr_offset, y))
            curr_offset += 1
        for y in range(min_y, max_y + 1):
            grid.pop((axis_n, y))


    elif axis == "y":
        curr_offset = 1
        min_x = min(x for x, y in grid)
        max_x = max(x for x, y in grid)
        while ((min_x, axis_n + curr_offset) in grid):
            for x in range(min_x, max_x + 1):
                existing = grid.get((x, axis_n - curr_offset), ".")
                updated = grid.get((x, axis_n + curr_offset), ".")

                if existing == "." and updated == ".":
                    new = "."
                else:
                    new = "#"
                
                grid[(x, axis_n - curr_offset)] = new
                grid.pop((x, axis_n + curr_offset))
            curr_offset += 1
        for x in range(min_x, max_x + 1):
            grid.pop((x, axis_n))
            

def print_grid(grid):
    min_x = min(x for x, y in grid)
    min_y = min(y for x, y in grid)

    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)

    for y in range(min_x, max_y + 1):
        for x in range(min_y, max_x + 1):
            print(grid[(x, y)], end="")
        print("")



def solve(input):
    raw_points, raw_folds = input
    grid = {}
    for p in raw_points:
        x, y = p.split(",")
        grid[(int(x), int(y))] = "#"
    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)

    print(max_x)
    print(max_y)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) not in grid:
                grid[(x, y)] = "."
    
    # print_grid(grid) 
    
    folds = []
    for f in raw_folds:
        axis, axis_n = f.replace("fold along ", "").split("=")
        folds.append((axis, int(axis_n)))
    
    first_fold = folds[0]
    process_fold(first_fold, grid)
    # print_grid(grid) 

    p1 = sum(1 for x, y in grid if grid[(x, y)] == "#")

    for f in folds[1:]:
        process_fold(f, grid)
        # print_grid(grid) 

    print_grid(grid) 

    return p1, None

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(13, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(13, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")