import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations, product
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
            with open("22/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/22/input.txt", "r") as f:
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

def parse_row(row, tups = False):
    op, coords = row.split(" ")
    x1, x2, y1, y2, z1, z2 = get_all_nums(coords)
    if tups:
        return op, ((x1, x2), (y1, y2), (z1, z2))
    return op, (x1, x2, y1, y2, z1, z2)

def get_cuboid_coords(x1, x2, y1, y2, z1, z2):
    return product(range(x1, x2 + 1), range(y1, y2 + 1), range(z1, z2 + 1))

def tamp(row):
    op, coords = row
    rec = []
    for c in coords:
        if c < -50:
            rec.append(-50)
        elif c > 50:
            rec.append(50)
        else:
            rec.append(c)
    return op, tuple(rec)

def solve1(input):
    rows = [parse_row(r) for r in input]
    filtered = []
    for op, coords in rows:
        print(coords)
        if all(abs(n) <= 50 for n in coords):
            filtered.append((op, coords))
    as_coords = [(t[0], get_cuboid_coords(*t[1])) for t in filtered]

    grid = {}
    for op, coords in as_coords:
        if op == "off":
            to_put = 0
        else:
            to_put = 1
        
        for c in coords:
            grid[c] = to_put
    
    p1 = sum(grid.values())

    return p1

def get_overlap(a1, a2):
    x1, x2 = a1
    y1, y2 = a2

    if x1 <= y2 and y1 <= x2:
        return (max(x1, y1), min(x2, y2))
    else:
        return None

def get_overlap_prism(c1, c2):
    x1, y1, z1 = c1
    x2, y2, z2 = c2

    xover = get_overlap(x1, x2)
    yover = get_overlap(y1, y2)
    zover = get_overlap(z1, z2)

    if xover and yover and zover:
        # print(f"overlap between {c1} and {c2}: {(xover, yover, zover)}")
        return (xover, yover, zover)
    return None

def inv_op(op):
    if op == "on":
        return "off"
    elif op == "off":
        return "on"
        
def red_op(op):
    if op == "on":
        return "on_red"
    elif op == "off":
        return "off_red"

def get_volume(c):
    (x1, x2), (y1, y2), (z1, z2) = c
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1) * (abs(z1 - z2) + 1)

def apply_row(op, coords, layers, curr_layer = 0):
    for same_cube in layers[curr_layer][op]:
        overlap = get_overlap_prism(coords, same_cube)
        if overlap:
            layers[curr_layer][red_op(op)].append(overlap)

    layers[curr_layer][op].append(coords)

    for opp_cube in layers[curr_layer][inv_op(op)]:
        overlap = get_overlap_prism(coords, opp_cube)
        if overlap:
            apply_row(op, overlap, layers, curr_layer + 1)

def solve2(input):
    rows = [parse_row(r, True) for r in input]
    print("num_rows: ", len(rows))

    on_cubes = []
    off_cubes = []
    for op, coords in rows:
        if op == "on":
            off_extend = []
            for on_cube in on_cubes:
                intersection = get_overlap_prism(on_cube, coords)
                if intersection:
                    off_extend.append(intersection)
            on_extend = []
            for off_cube in off_cubes:
                intersection = get_overlap_prism(off_cube, coords)
                if intersection:
                    on_extend.append(intersection)
            off_cubes.extend(off_extend)
            on_cubes.extend(on_extend)
            on_cubes.append(coords)
        elif op == "off":
            off_extend = []
            for on_cube in on_cubes:
                intersection = get_overlap_prism(on_cube, coords)
                if intersection:
                    off_extend.append(intersection)
            on_extend = []
            for off_cube in off_cubes:
                intersection = get_overlap_prism(off_cube, coords)
                if intersection:
                    on_extend.append(intersection)
            off_cubes.extend(off_extend)
            on_cubes.extend(on_extend)
    
    return sum(get_volume(c) for c in on_cubes) - sum(get_volume(c) for c in off_cubes)

start = time.time()
answer1 = solve1(input)
answer2 = solve2(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(22, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(22, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")