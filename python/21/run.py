import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations, product
from functools import lru_cache
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
            with open("21/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/21/input.txt", "r") as f:
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

class ddie:
    def __init__(self):
        self.roll = 1
        self.num_rolls = 0
    
    def do_roll(self):
        self.num_rolls += 1
        curr = self.roll
        self.roll += 1
        if self.roll > 100:
            self.roll -= 100
        return curr
    
    def roll3(self):
        r1 = self.do_roll()
        r2 = self.do_roll()
        r3 = self.do_roll()
        return r1 + r2 + r3
        
def solve1(input):
    p1_pos = int(get_all_nums(input[0])[1])
    p2_pos = int(get_all_nums(input[1])[1])
    # print(p1_pos, p2_pos)
    p1_pts = 0
    p2_pts = 0

    die = ddie()
    while p1_pts < 1000 and p2_pts < 1000:
        roll = die.roll3()
        p1_pos = (p1_pos + roll) % 10
        if p1_pos == 0:
            p1_pos = 10
        p1_pts += p1_pos
        if p1_pts >= 1000:
            break

        roll = die.roll3()
        p2_pos = (p2_pos + roll) % 10
        if p2_pos == 0:
            p2_pos = 10
        p2_pts += p2_pos
    
    print(die.num_rolls)
    print(p1_pts, p2_pts)
    p1 = die.num_rolls * min(p1_pts, p2_pts)

    return p1

qdie_rolls = product([1, 2, 3], repeat=3)
qdie_outcome = [sum(r) for r in qdie_rolls]

@lru_cache(maxsize=None)
def recurse(p1s_turn, prev_roll, p1_pos, p2_pos, p1_pts, p2_pts):
    if p1s_turn:
        updated_p1_pos = (p1_pos + prev_roll) % 10
        if updated_p1_pos == 0:
            updated_p1_pos = 10
        updated_p2_pos = p2_pos
    else:
        updated_p2_pos = (p2_pos + prev_roll) % 10
        if updated_p2_pos == 0:
            updated_p2_pos = 10
        updated_p1_pos = p1_pos

    if p1s_turn:
        updated_p1_pts = p1_pts + updated_p1_pos
        updated_p2_pts = p2_pts
    else:
        updated_p2_pts = p2_pts + updated_p2_pos
        updated_p1_pts = p1_pts

    if p1s_turn and updated_p1_pts >= 21:
        return [1, 0]
    elif not p1s_turn and updated_p2_pts >= 21:
        return [0, 1]
    
    outcomes = [0, 0]
    for r in qdie_outcome:
        p1_wins, p2_wins = recurse(not p1s_turn, r, updated_p1_pos, updated_p2_pos, updated_p1_pts, updated_p2_pts)
        outcomes[0] += p1_wins
        outcomes[1] += p2_wins
    return outcomes

def solve2(input):
    p1_pos = int(get_all_nums(input[0])[1])
    p2_pos = int(get_all_nums(input[1])[1])

    outcomes = [0, 0]
    for r in qdie_outcome:
        p1_wins, p2_wins = recurse(True, r, p1_pos, p2_pos, 0, 0)
        outcomes[0] += p1_wins
        outcomes[1] += p2_wins
    return max(outcomes[0], outcomes[1])

def solve3(input):
    p1_pos = int(get_all_nums(input[0])[1])
    p2_pos = int(get_all_nums(input[1])[1])

    state_map = {
        (p1_pos, 0, p2_pos, 0): 1
    }

start = time.time()
answer1 = solve1(input)
answer2 = solve2(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(21, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(21, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")