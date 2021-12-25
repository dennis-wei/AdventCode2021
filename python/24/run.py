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
            with open("24/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/24/input.txt", "r") as f:
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

def parse_input(input):
    if "inp" in input:
        return input.split(" ")
    op, var1, var2 = input.split(" ")
    if var2 not in "wxyz":
        mode = "constant"
        var2 = int(var2)
    else:
        mode = "variable"
    return op, mode, var1, var2

class Program:
    def __init__(self, commands):
        self.vars = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0
        }
        self.ip = 0
        self.commands = [parse_input(c) for c in commands]
        self.init_commands = deepcopy(self.commands)
    
    def reset(self):
        self.vars = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0
        }
        self.ip = 0
        self.commands = deepcopy(self.init_commands)
    
    def handle_command(self, inputs, command, verbose = False):
        self.ip += 1
        if len(command) == 2:
            print(self.vars)
            var = command[1]
            # print(var)
            # print(inputs)
            self.vars[var] = inputs.pop(0)
            return inputs
        
        if verbose and command[:3] == ("add", "constant", "x"):
            print(f"adding {command[3]} to x")

        if verbose and command[:3] == ("add", "constant", "y") and command[3] != 25 and command[3] != 1:
            print(f"adding {command[3]} to y")

        if verbose and command == ("eql", "variable", "x", "w"):
            print("z%26: ", self.vars["z"] % 26)
            print("x: ", self.vars["x"])
            print("w: ", self.vars["w"])
            print("x == w: ", self.vars["x"] == self.vars["w"])

        op, mode, raw_var1, raw_var2 = command
        var1 = self.vars[raw_var1]
        if mode == "variable":
            var2 = self.vars[raw_var2]
        elif mode == "constant":
            var2 = raw_var2
            
        # print(self.vars)
        # print(command)
        # print(var1, var2)
        
        if op == "mul":
            self.vars[raw_var1] = var1 * var2
        elif op == "add":
            self.vars[raw_var1] = var1 + var2
        elif op == "div":
            if var2 == 0:
                raise
            self.vars[raw_var1] = var1 // var2
        elif op == "mod":
            if var1 < 0 or var2 <= 0:
                raise
            self.vars[raw_var1] = var1 % var2
        elif op == "eql":
            self.vars[raw_var1] = int(var1 == var2)

        if verbose and command == ("add", "variable", "z", "y"):
            print("z%26: ", self.vars["z"] %26 )
        return inputs
    
    def run(self, inputs):
        for c in self.commands:
            inputs = self.handle_command(inputs, c)
        print("end")
        print(self.vars)
        if self.vars["z"] == 0:
            return True
        return False

def run_tests():
    test = ["inp x", "mul x -1"]
    test_program = Program(test)
    test_program.run([-1])

    test = """
    inp z
    inp x
    mul z 3
    eql z x
    """.strip().split("\n")
    test_program = Program(test)
    test_program.run([1, 3])

    test = """
    inp w
    add z w
    mod z 2
    div w 2
    add y w
    mod y 2
    div w 2
    add x w
    mod x 2
    div w 2
    mod w 2
    """.strip().split("\n")
    test_program = Program(test)
    test_program.run([14])

program_tuples = [
    (1, 14, 12),
    (1, 10, 9),
    (1, 13, 8),
    (26, -8, 3),
    (1, 11, 0),
    (1, 11, 11),
    (1, 14, 10),
    (26, -11, 13),
    (1, 14, 3),
    (26, -1, 10),
    (1, 14, 3),
    (26, -1, 10),
    (26, -8, 10),
    (26, -5, 14),
    (26, -16, 6),
    (26, -6, 5)
]

def concise_program(input):
    z = 0
    for i, (a, b, c) in zip(input, program_tuples):
        z = z // a
        if a == 26 and z % 26 + b != i:
            return False
        if z % 26 + b != i:
            z = z * 26 + i + c
    return z == 0 

def solve(input):
    program = Program(input)
    program.run([int(c) for c in "39999698799429"])
    program.reset()
    program.run([int(c) for c in "18116121134117"])
    return 39999698799429, 18116121134117

start = time.time()
answer1, answer2 = solve(input)

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(24, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(24, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")