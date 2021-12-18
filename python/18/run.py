import time
import os, sys
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations, permutations
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
            with open("18/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/18/input.txt", "r") as f:
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

def add(t1, t2):
    return "[" + t1 + "," + t2 + "]"

def explode(t):
    rec_depth = 0
    num_acc = ""
    encountered_nums = []
    found = False
    explode_indices = None, None
    for i, c in enumerate(t):
        if c == "[":
            rec_depth += 1
        elif c in "0123456789":
            num_acc += c
        elif c == ",":
            if num_acc != "":
                encountered_nums.append(((i - len(num_acc), i), num_acc))
            num_acc = ""
        elif c == "]":
            if num_acc != "":
                encountered_nums.append(((i - len(num_acc), i), num_acc))
            num_acc = ""
            if rec_depth > 4 and found == False:
                found = True
                explode_indices = len(encountered_nums) - 2, len(encountered_nums) - 1
            rec_depth -= 1

    if not found:
        return None
    
    
    left_num_idx, right_num_idx = explode_indices
    (left_start_idx, left_end_idx), left_num = encountered_nums[left_num_idx]
    (right_start_idx, right_end_idx), right_num = encountered_nums[right_num_idx]

    updated = t
    idx_delta = 0
    if left_num_idx != 0:
        (prior_start_idx, prior_end_idx), prior_num = encountered_nums[left_num_idx - 1]
        res = str(int(left_num) + int(prior_num))
        updated = t[:prior_start_idx] + res + t[prior_end_idx:]
        idx_delta = len(res) - (prior_end_idx - prior_start_idx)
    
    tuple_start_idx = left_start_idx - 1 + idx_delta
    tuple_end_idx = right_end_idx + 1 + idx_delta
    updated = updated[:tuple_start_idx] + "0" + updated[tuple_end_idx:]
    idx_delta -= (tuple_end_idx - tuple_start_idx - 1)

    if right_num_idx != len(encountered_nums) - 1:
        (post_start_idx, post_end_idx), post_num = encountered_nums[right_num_idx + 1]
        post_start_idx += idx_delta
        post_end_idx += idx_delta
        res = str(int(right_num) + int(post_num))
        updated = updated[:post_start_idx] + res + updated[post_end_idx:]
    
    return updated

def split(t):
    num_acc = ""
    encountered_nums = []
    found = False
    split_num_idx, split_num = None, None
    for i, c in enumerate(t):
        if c in "0123456789":
            num_acc += c
        elif c == ",":
            if num_acc != "":
                encountered_nums.append(((i - len(num_acc), i), num_acc))
                if len(num_acc) >= 2 and not found:
                    split_num_idx, split_num = len(encountered_nums) - 1, num_acc
                    found = True
                    break
            num_acc = ""
        elif c == "]":
            if num_acc != "":
                encountered_nums.append(((i - len(num_acc), i), num_acc))
                if len(num_acc) >= 2 and not found:
                    split_num_idx, split_num = len(encountered_nums) - 1, num_acc
                    found = True
                    break
            num_acc = ""
    
    if not found:
        return None
    
    replacement = f"[{floor(int(split_num)/2)},{ceil(int(split_num)/2)}]"
    start_idx, end_idx = encountered_nums[split_num_idx][0]
    
    return t[:start_idx] + replacement + t[end_idx:]

def reduce(t):
    explode_result = explode(t)
    if explode_result:
        return reduce(explode_result)
    split_result = split(t)
    if split_result:
        return reduce(split_result)
    return t

pattern = re.compile("\[\d+,\d+\]")
def calculate(t):
    matches = re.findall(pattern, t)
    if not matches:
        return t

    updated = t
    for m in matches:
        n1, n2 = get_all_nums(m)
        updated = updated.replace(m, str(3*n1 + 2*n2))
    return calculate(updated)

def part1(input):
    res = input[0]
    # print(res)
    for t in input[1:]:
        added = add(res, t)
        # print("post add: ", added)
        res = reduce(added)
        # print(res)
    return calculate(res)

def part2(input):
    max_res = -1
    for sn1, sn2 in permutations(input, 2):
        res = int(calculate(reduce(add(sn1, sn2))))
        if res > max_res:
            max_res = res
    return max_res

def solve(input):
    return part1(input), part2(input)

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(18, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(18, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")