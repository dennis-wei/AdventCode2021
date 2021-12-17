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
    for filename in ("input.txt", "17/input.txt", "python/17/input.txt"):
        try:
            with open(filename, "r") as f:
                raw_input = f.read()
                break
        except:
            continue
raw_input = raw_input.strip()

input = (
    Input(raw_input)
        # .ints()
        # .int_tokens()
        .tokens()
        # .lines()
        # .line_tokens()
        # .line_tokens(sep = "\n", line_sep = "\n\n")
)

def simulate(target_area, hax, ly, xv, yv):
    x = 0
    y = 0
    max_y = 0
    while y > ly and abs(x) < hax:
        x += xv
        y += yv
        if y > max_y:
            max_y = y
        if (x, y) in target_area:
            return True, max_y
        if xv == 0:
            xv = 0
        elif x > 0:
            xv -= 1
        elif x < 0:
            xv += 1
        yv -= 1
    return False, max_y

def solve(input):
    x1, x2 = [int(n) for n in input[2].replace(",", "").replace("x=", "").split("..")]
    lx = x1 if x1 < x2 else x2
    hx = x1 if x1 > x2 else x2

    y1, y2 = [int(n) for n in input[3].replace(",", "").replace("y=", "").split("..")]
    ly = y1 if y1 < y2 else y2
    hy = y1 if y1 > y2 else y2

    hax = max(abs(lx), abs(hx))
    hay = max(abs(ly), abs(hy))

    print("xrange: ", lx, hx)
    print("yrange: ", ly, hy)

    target = set()
    for x in range(lx, hx + 1):
        for y in range(ly, hy + 1):
            target.add((x, y))
    
    highest_y = -1
    best_option = (-1, -1)
    num_work = 0

    if hx > 0:
        x_range = range(hax + 1)
    else:
        x_range = range(0, -hax - 1, -1)
    for ix in x_range:
        for iy in range(-hay, hay + 1):
            hit_target, my = simulate(target, hax, ly, ix, iy)
            if hit_target:
                num_work += 1
                if my > highest_y:
                    highest_y = my
                    best_option = (ix, iy)

    print(best_option, highest_y)
    print(num_work)

    return highest_y, num_work

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(17, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(17, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")