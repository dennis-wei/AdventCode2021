import time
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import argparse
import clipboard

from itertools import combinations, permutations, product
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
            with open("19/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/19/input.txt", "r") as f:
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

class Scanner:
    def __init__(self, input, dims = 3):
        base = [[int(n) for n in i.split(",")] for i in input[1:]]
        if dims == 2:
            tups = [(x, y, 0) for x, y in base]
        else:
            tups = base
        self.tups = tups
        self.initial_tups = deepcopy(self.tups)
        self.id = get_all_nums(input[0])[0]
        self.rot = 0
        self.fingerprints = self.make_fingerprints()
    
    def make_fingerprints(self):
        prints = {}
        for t1, t2 in permutations(self.tups, 2):
            x1, y1, z1 = t1
            x2, y2, z2 = t2
            prints[abs(x1-x2)**2 + abs(y1-y2)**2 + abs(z1-z2)**2] = (t1, t2)
        return prints
    
    def swap_lead(self, to_swap):
        new_tups = []
        if to_swap == 1:
            for (x, y, z) in self.initial_tups:
                new_tups.append((-y, z, -x))
        elif to_swap == 2:
            for (x, y, z) in self.initial_tups:
                new_tups.append((-z, y, x))
        return new_tups
    
    def apply_axis_rot(self):
        new_tups = []
        parity = self.rot % 8
        if parity in [1, 3, 5, 7]:
            for (x, y, z) in self.tups:
                new_tups.append((x, -y, -z))
        elif parity in [2, 6]:
            for (x, y, z) in self.tups:
                new_tups.append((x, -z, y))
        elif parity == 4:
            for (x, y, z) in self.tups:
                new_tups.append((-x, -z, -y))
        return new_tups

    def rotate(self):
        self.rot += 1
        if self.rot == 8:
            self.tups = self.swap_lead(1)
        elif self.rot == 16:
            self.tups = self.swap_lead(2)
        elif self.rot == 24:
            print("Went through all rotations for scanner ", self.id)
            self.rot = 0
            return True
        else:
            self.tups = self.apply_axis_rot()
        return False
    
    def apply_basis(self, basis):
        dx, dy, dz = basis
        res = set()
        for x, y, z in self.tups:
            res.add((x + dx, y + dy, z + dz))
        return res

def get_rep(base_point, tups):
    (bx, by, bz) = base_point
    transformed = set()
    for (x, y, z) in tups:
        tx = x - bx
        ty = y - by
        tz = z - bz
        transformed.add((tx, ty, tz))
    return transformed

def solve(input):
    scanners = [Scanner(i) for i in input]
    scanners_map = {s.id: s for s in scanners}
    unfound = set(s.id for s in scanners[1:])
    found = set([scanners[0].id])
    tested = set()
    worked_mapping = {}
    while len(unfound) > 0:
        added = False
        for s2_id in unfound:
            s2 = scanners_map[s2_id]
            sol_found = False
            for s1_id in found:
                if (s1_id, s2_id) in tested:
                    continue
                done = False
                s1 = scanners_map[s1_id]
                shared_prints = s1.fingerprints.keys() & s2.fingerprints.keys()
                if len(shared_prints) < 12:
                    continue
                while not done:
                    for bp1, bp2 in product(s1.tups, s2.tups):
                        if done:
                            break

                        rep1 = get_rep(bp1, s1.tups)
                        rep2 = get_rep(bp2, s2.tups)

                        if len(rep1 & rep2) >= 6:
                            done = True
                            sol_found = True
                            added = True
                            unfound.remove(s2_id)
                            found.add(s2_id)
                            worked_mapping[(s1_id, s2_id)] = (bp1, bp2)
                            break
                    if not done:
                        done = s2.rotate()
                tested.add((s1_id, s2_id))
                if sol_found:
                    break
            if sol_found:
                break
        if not added:
            print("Did complete loop without adding")
            print("Still unfound: ", unfound)
            break

    coords = {0: (0,0,0)}
    while len(coords) < len(found):
        for (s1_id, s2_id), (t1, t2) in worked_mapping.items():
            if s1_id in coords and s2_id not in coords:
                (x1, y1, z1) = t1
                (x2, y2, z2) = t2
                xd = x1 - x2
                yd = y1 - y2
                zd = z1 - z2

                bx, by, bz = coords[s1_id]

                coords[s2_id] = (bx + xd, by + yd, bz + zd)

    all_beacons = set()
    for (s, basis) in coords.items():
        all_beacons = all_beacons.union(scanners_map[s].apply_basis(basis))
    
    p2 = -1
    for s1, s2 in permutations(coords.keys(), 2):
        x1, y1, z1 = coords[s1]
        x2, y2, z2 = coords[s2]
        dist = abs(x1-x2) + abs(y1-y2) + abs(z1 - z2)
        if dist > p2:
            p2 = dist

    return len(all_beacons), p2
    
start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(19, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(19, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")