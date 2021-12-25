from re import S
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
import random

import networkx as nx

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
            with open("23/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/23/input.txt", "r") as f:
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

def get_starting_state_part1(input):
    cl = [[c for c in line if c in ".ABCD"] for line in input[2:-1]]
    return "".join([
        ".", ".", # left hallway
        cl[0][0], cl[1][0], # A aisle
        ".",
        cl[0][1], cl[1][1], # B aisle
        ".",
        cl[0][2], cl[1][2], # C aisle
        ".",
        cl[0][3], cl[1][3], # D aisle
        ".", "." # right hallway
    ])

def get_starting_state_part2(input):
    cl = [[c for c in line if c in ".ABCD"] for line in input[2:-1]]
    return "".join([
        ".", ".", # left hallway
        cl[0][0], cl[1][0], cl[2][0], cl[3][0], # A aisle
        ".",
        cl[0][1], cl[1][1], cl[2][1], cl[3][1], # B aisle
        ".",
        cl[0][2], cl[1][2], cl[2][2], cl[3][2], # C aisle
        ".",
        cl[0][3], cl[1][3], cl[2][3], cl[3][3], # D aisle
        ".", "." # right hallway
    ])

def state_str(state):
    return "".join(state)

def print_state_part1(s):
    print("#############")
    print(f"#{s[0]}{s[1]}.{s[4]}.{s[7]}.{s[10]}.{s[13]}{s[14]}#")
    print(f"###{s[2]}#{s[5]}#{s[8]}#{s[11]}###")
    print(f"  #{s[3]}#{s[6]}#{s[9]}#{s[12]}#  ")
    print("  #########  ")
    print()

def print_state_part2(s):
    print("#############")
    print(f"#{s[0]}{s[1]}.{s[6]}.{s[11]}.{s[16]}.{s[21]}{s[22]}#")
    print(f"###{s[2]}#{s[7]}#{s[12]}#{s[17]}###")
    print(f"  #{s[3]}#{s[8]}#{s[13]}#{s[18]}#  ")
    print(f"  #{s[4]}#{s[9]}#{s[14]}#{s[19]}#  ")
    print(f"  #{s[5]}#{s[10]}#{s[15]}#{s[20]}#  ")
    print("  #########  ")
    print()

def print_state(s, part = 1):
    if part == 1:
        print_state_part1(s)
    elif part == 2:
        print_state_part2(s)

cost = {"A": 1, "B": 10, "C": 100, "D": 1000}

base_grid1 = {
    0: {1: 1},
    1: {0: 1, 2: 2, 4: 2},
    2: {1: 2, 3: 1, 4: 2},
    3: {2: 1},
    4: {1: 2, 2: 2, 5: 2, 7: 2},
    5: {4: 2, 6: 1, 7: 2},
    6: {5: 1},
    7: {4: 2, 5: 2, 8: 2, 10: 2},
    8: {7: 2, 9: 1, 10: 2},
    9: {8: 1},
    10: {7: 2, 8: 2, 11: 2, 13: 2},
    11: {10: 2, 12: 1, 13: 2},
    12: {11: 1},
    13: {10: 2, 11: 2, 14: 1},
    14: {13: 1}
}
hallway1 = set([0, 1, 4, 7, 10, 13, 14])
firstrow1 = set([2, 5, 8, 11])
secondrow1 = set([3, 6, 9, 12])
aisles1 = {
    2: "A",
    3: "A",
    5: "B",
    6: "B",
    8: "C",
    9: "C",
    11: "D",
    12: "D"
}

base_grid2 = {
    0: {1: 1},
    1: {0: 1, 2: 2, 6: 2},
    2: {1: 2, 3: 1, 6: 2},
    3: {2: 1, 4: 1},
    4: {3: 1, 5: 1},
    5: {4: 1},
    6: {1: 2, 2: 2, 7: 2, 11: 2},
    7: {6: 2, 8: 1, 11: 2},
    8: {7: 1, 9: 1},
    9: {8: 1, 10: 1},
    10: {9: 1},
    11: {6: 2, 7: 2, 12: 2, 16: 2},
    12: {11: 2, 13: 1, 16: 2},
    13: {12: 1, 14: 1},
    14: {13: 1, 15: 1},
    15: {14: 1},
    16: {11: 2, 12: 2, 17: 2, 21: 2},
    17: {16: 2, 18: 1, 21: 2},
    18: {17: 1, 19: 1},
    19: {18: 1, 20: 1},
    20: {19: 1},
    21: {16: 2, 19: 2, 22: 1},
    22: {21: 1}
}
hallway2 = set([0, 1, 6, 11, 16, 21, 22])
firstrow2 = set([2, 7, 12, 17])
secondrow2 = set([3, 8, 13, 18])
thirdrow2 = set([4, 9, 14, 19])
fourthrow2 = set([5, 10, 15, 20])
aisles2 = {
    2: "A", 3: "A", 4: "A", 5: "A",
    7: "B", 8: "B", 9: "B", 10: "B",
    12: "C", 13: "C", 14: "C", 15: "C",
    17: "D", 18: "D", 19: "D", 20: "D",
}

def get_filtered_neighbors_part1(state, i, c):
    if i in firstrow1 and aisles1[i] == c and state[i+1] == ".":
        return [(i + 1, 1)]
    if i in firstrow1 and aisles1[i] == c and state[i+1] == c:
        return []
    if i in secondrow1 and aisles1[i] == c:
        return []

    unfiltered = base_grid1[i].items()
    empty = [n for n in unfiltered if state[n[0]] == "."]
    if i in hallway1:
        aisle_filtered = []
        for n in empty:
            if n[0] in hallway1:
                aisle_filtered.append(n)
            elif aisles1[n[0]] == c and state[n[0] + 1] == "." or state[n[0] + 1] == c:
                aisle_filtered.append(n)
    else:
        if i in firstrow1 and aisles1[i] != c:
            aisle_filtered = [n for n in empty if n[0] in hallway1]
        else:
            aisle_filtered = empty
    return aisle_filtered

def get_filtered_neighbors_part2(state, i, c):
    if i in fourthrow2:
        if aisles2[i] == c:
            return []
        elif state[i - 1] == ".":
            return [(i - 1, 1)]
        else:
            return []
    
    elif i in thirdrow2:
        if aisles2[i] == c:
            if all(state[d] in [".", c] for d in [i + 1]):
                if state[i+1] == ".":
                    return [(i+1, 1)]
                else:
                    return []
            elif state[i-1] == ".":
                if any(state[d] not in [".", c] for d in [i + 1]):
                    return [(i-1, 1)]
                else:
                    return []
            else:
                return []
        else:
            if state[i - 1] == ".":
                return [(i - 1, 1)]
            else:
                return []
                

    elif i in secondrow2:
        if aisles2[i] == c:
            if all(state[d] in [".", c] for d in [i + 1, i + 2]):
                if state[i+1] == ".":
                    return [(i+1, 1)]
                else:
                    return []
            elif state[i-1] == ".":
                if any(state[d] not in [".", c] for d in [i + 1, i + 2]):
                    return [(i-1, 1)]
                else:
                    return []
            else:
                return []
        else:
            if state[i - 1] == ".":
                return [(i - 1, 1)]
            else:
                return []

    elif i in firstrow2 and aisles2[i] == c:
        if all(state[d] in [".", c] for d in [i + 1, i + 2, i + 3]):
            if state[i+1] == ".":
                return [(i+1, 1)]
            else:
                return []

    unfiltered = base_grid2[i].items()
    empty = [n for n in unfiltered if state[n[0]] == "."]
    if i in hallway2:
        aisle_filtered = []
        for n in empty:
            if n[0] in hallway2:
                aisle_filtered.append(n)
            elif aisles2[n[0]] == c and all(state[d] in [".", c] for d in [n[0], n[0] + 1, n[0] + 2, n[0] + 3]):
                aisle_filtered.append(n)
    else:
        if i in firstrow2 and aisles2[i] != c:
            aisle_filtered = [n for n in empty if n[0] in hallway2]
        else:
            aisle_filtered = empty
    return aisle_filtered

def apply_move(state, i, c, n):
    new_state = list(state)
    new_state[i] = "."
    new_state[n] = c
    return "".join(new_state)

def populate_graph(g, queue, queued, part = 1, verbose = False):
    num_iters = 0
    while len(queue) > 0:
        num_iters += 1
        state, cost_thus_far, num_moves_so_far = queue.pop(0)
        g.add_node(state)
        for i, c in enumerate(state):
            if c == ".":
                continue
            
            if part == 1:
                neighbors = get_filtered_neighbors_part1(state, i, c)
            elif part == 2:
                neighbors = get_filtered_neighbors_part2(state, i, c)

            for n in neighbors:
                updated_state = apply_move(state, i, c, n[0])
                new_cost = n[1] * cost[c]
                total_cost = cost_thus_far + new_cost

                if updated_state not in queued and total_cost < 50000 and num_moves_so_far < 115:
                    g.add_node(updated_state)
                    g.add_edge(state, updated_state, weight=new_cost)
                    queue.append((updated_state, total_cost, num_moves_so_far + 1))
                    queued.add(updated_state)
        num_iters += 1
        if num_iters % 100000 == 0:
            print(num_iters)

    if verbose: 
        print("queue")
        for n in queue:
            print_state(n, part)

def solve(filename, part = 1, verbose = False):
    with open(filename, "r") as f:
        input = Input(f.read()).lines()
    g = nx.Graph()
    if part == 1:
        starting_state = get_starting_state_part1(input)
    if part == 2:
        starting_state = get_starting_state_part2(input)
            
    populate_graph(g, [(starting_state, 0, 0)], set(starting_state), part, verbose)

    print(len(g.nodes))

    print("graph constructed, getting path")
    if part == 1:
        ending_state = "..AA.BB.CC.DD.."
    elif part == 2:
        ending_state = "..AAAA.BBBB.CCCC.DDDD.."
        checkpoints =[
            "BADDDC.CCBD.ABAA...CB..",
            "BADDDC.CCBD.ABAA...CB..",
            "BADDDC.CCBD.ABAA..C.B..",
            "BADDDC.CCBD.ABAA.C..B..",
            "BADDDC.CCBD.ABAA....BC.",
            "BADDDC.CCBD.ABAA....B.C",
            "BADDDC.CCBD.ABAA.....BC",
            "BA.....CCBD.ABAAC.DDDBC",
            "B..A.A.CCBD..BAAC.DDDBC",
            "B...AA.CCBD..BAAC.DDDBC", # worked at 100 moves
            "BB..AA.CCBD...AAC.DDDBC",
            "BB.AAA.CCBD....AC.DDDBC",
            "BBAAAA.CCBD.....C.DDDBC",
            "BBAAAA.CCBD.....C.DDDBC",
            "BBAAAAB...D..CCC..DDDBC", # worked
            "BBAAAAB......CCC.DDDDBC",
            "..AAAAB..BB..CCC.DDDDBC",
            "..AAAA..BBB..CCC.DDDDBC",
            "..AAAA..BBB..CCCBDDDD.C",
            "..AAAA..BBBB.CCC.DDDD.C",
            "..AAAA.BBBB..CCC.DDDD.C",
            "..AAAA.BBBB..CCC.DDDDC.",
            "..AAAA.BBBB.CCCC.DDDD.."
        ]
        for c in checkpoints:
            if not c in g.nodes:
                print(f"checkpoint {c} not in nodes")
                raise Exception
    best_path = nx.single_source_dijkstra(g, source=starting_state, target=ending_state)
    for s in best_path[1]:
        print_state(s, part)
    print(best_path[0])

    return best_path[0]

start = time.time()
# print("Part 1")
# answer1 = solve("input.txt", 1)
print("Part 2")
answer2 = solve("input2.txt", 2)

print(f"Answer: {answer2}")
# print(submit(23, 1, answer1).text)

print(f"Answer: {answer2}")
# print(submit(23, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")