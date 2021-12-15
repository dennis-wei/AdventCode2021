import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard
import networkx as nx

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
            with open("15/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/15/input.txt", "r") as f:
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

def solve(grid):
    graph = nx.DiGraph()
    graph.add_nodes_from(grid.keys())
    
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for x, y in grid:
        for dx, dy in neighbors:
            mx = x + dx
            my = y + dy
            if (mx, my) in grid:
                graph.add_edge((x, y), (mx, my), weight=grid[(mx, my)])
    
    max_x = max(t[0] for t in grid)
    max_y = max(t[1] for t in grid)
    return nx.single_source_dijkstra(graph, source = (0, 0), target = (max_x, max_y), weight="weight")[0]

def make_grid(input, replication_factor = 1):
    len_y = len(input)
    len_x = len(input[0])

    grid = {}
    for i, row in enumerate(input):
        for j, c in enumerate(row):
            for k in range(replication_factor):
                for l in range(replication_factor):
                    risk = (int(c) + k + l) % 9
                    if risk == 0:
                        risk = 9
                    grid[(j + k * len_x, i + l * len_y)] = risk
    
    return grid

answer1 = solve(make_grid(input, 1))
answer2 = solve(make_grid(input, 5))

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(15, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(15, 2, answer1).text)
# print(f"Took {time.time() - start} seconds for both parts")