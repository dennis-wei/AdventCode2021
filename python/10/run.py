import time
import math
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
        with open("python/10/input.txt", "r") as f:
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

matches = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>',
}
inv_matches = {v: k for k, v in matches.items()}

points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

def do_p1(line):
    stack = []
    for c in line:
        if c in matches:
            stack.append(c)
        elif c in inv_matches:
            matching = stack.pop()
            if not matches[matching] == c:
                return (True, c)
    return (False, stack)

points2 = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,

}

def score(stack):
    acc = 0
    for c in stack[::-1]:
        acc *= 5
        acc += points2[c]
    return acc


def solve(input):
    p1_all = [do_p1(line) for line in input]
    p1_filtered = [l for l in p1_all if l[0]]
    p1 = sum(points[l[1]] for l in p1_filtered)

    p2_lines = [l for l in p1_all if not l[0]]
    p2_scores = sorted([score(l[1]) for l in p2_lines])
    med_index = math.floor(len(p2_scores) / 2)
    return p1, p2_scores[med_index]

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(10, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(10, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")