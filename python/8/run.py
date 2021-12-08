import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations, permutations
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
            with open("8/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/8/input.txt", "r") as f:
                raw_input  = f.read()
raw_input = raw_input.strip()

input = (
    Input(raw_input)
        .all()
        # .ints()
        # .int_tokens()
        # .tokens()
        # .lines()
        # .line_tokens()
        # .line_tokens(sep = "\n", line_sep = "\n\n")
)

segment_mapping = {
    frozenset([1, 2, 3, 5, 6, 7]): 0,
    frozenset([3, 6]): 1,
    frozenset([2, 3, 4, 5, 7]): 2,
    frozenset([2, 3, 4, 6, 7]): 3,
    frozenset([1, 3, 4, 6]): 4,
    frozenset([1, 2, 4, 6, 7]): 5,
    frozenset([1, 2, 4, 5, 6, 7]): 6,
    frozenset([2, 3, 6]): 7,
    frozenset([1, 2, 3, 4, 5, 6, 7]): 8,
    frozenset([1, 2, 3, 4, 6, 7]): 9
}

valid_nums = set(segment_mapping.keys())

def process(row):
    signal, output = row
    for opt in permutations("abcdefg"):
        mapping_valid = True
        mapping = {r[0]: r[1] for r in zip(opt, [1, 2, 3, 4, 5, 6, 7])}
        for s in signal:
            segments = frozenset([mapping[c] for c in s])
            if not segments in valid_nums:
                mapping_valid = False
                break

        if mapping_valid:
            break
    
    res = ""
    for o in output:
        segments = frozenset([mapping[c] for c in o])
        res += str(segment_mapping[segments])
    return int(res)
    
def solve(input):
    input = [r for r in input.replace("|\n", "| ").split("\n")]

    rows = []
    for r in input:
        signal, output = (x.split(" ") for x in r.strip().split(" | "))
        signal = sorted(signal, key = lambda x: len(x))
        rows.append((signal, output))
    
    p1_acc = 0
    for r in rows:
        output = r[1]
        p1_acc += len([1 for m in output if len(m) in set([2, 4, 3, 7])])
    
    # process(rows[0])
    p2 = sum(process(r) for r in rows)

    return p1_acc, p2

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(8, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(8, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")