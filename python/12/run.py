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
            with open("12/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/12/input.txt", "r") as f:
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

def extract_graph(input):
    small_nodes = set()
    edges = defaultdict(set)
    for line in input:
        (a, b) = line.split("-")
        if(a.lower() == a):
            small_nodes.add(a)
        if(b.lower() == b):
            small_nodes.add(b)
        edges[a].add(b)
        edges[b].add(a)
    return small_nodes, edges

def pt2_valid_small_node(visited_counts, attempted_node):
    if attempted_node == "start":
        return False

    if attempted_node not in visited_counts:
        return True
    
    if 2 not in visited_counts.values():
        return True
    
    return False

def traverse(curr_node, small_nodes, edges, visited_counts, neighbor_filter):
    updated_visited_counts = visited_counts.copy()
    if curr_node in small_nodes:
        updated_visited_counts[curr_node] += 1
    if curr_node == "end":
        return 1

    valid_neighbors = list(filter(lambda x: neighbor_filter(x, updated_visited_counts), edges[curr_node]))

    acc = 0
    for neighbor in valid_neighbors:
        acc += traverse(neighbor, small_nodes, edges, updated_visited_counts, neighbor_filter)
    return acc

def solve(input):
    small_nodes, edges = extract_graph(input)

    p1 = traverse("start", small_nodes, edges, defaultdict(int), lambda x, y: x not in y)
    p2 = traverse("start", small_nodes, edges, defaultdict(int), lambda x, y: pt2_valid_small_node(y, x))
    return p1, p2

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(12, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(12, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")