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
            with open("16/input.txt", "r") as f:
                raw_input = f.read()
        except:
            with open("python/16/input.txt", "r") as f:
                raw_input = f.read()
raw_input = raw_input.strip()

input = (
    Input(raw_input)
        .all()
        # .ints()
        # .int_tokens()
        # .tokens()
        # .lines()
        # .line_tokens()
        # .line_tokens(sep: "\n", line_sep: "\n\n")
)

mapping = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}

def parse_input(input):
    acc = ""
    for c in input:
        acc += mapping[c]
    return acc

def handle_literal_packet(packet_version, input):
    i = 0
    chunk_acc = ""
    next_chunk = input[i:i+5]
    ending = False
    while not ending:
        ending = next_chunk[0] == "0"
        literal = next_chunk[1:]
        chunk_acc += literal
        i += 5
        next_chunk = input[i:i+5]

    return [(packet_version, int(chunk_acc, 2))], input[i:]

def do_reduce(args, packet_type):
    packet_version_sum = sum(t[0] for t in args)

    op_args = [t[1] for t in args[1:]]
    if packet_type == 0:
        res = sum(op_args)
    elif packet_type == 1:
        res = reduce(lambda x, y: x * y, op_args, 1)
    elif packet_type == 2:
        res = min(op_args)
    elif packet_type == 3:
        res = max(op_args)
    elif packet_type == 5:
        res = int(op_args[0] > op_args[1])
    elif packet_type == 6:
        res = int(op_args[0] < op_args[1])
    elif packet_type == 7:
        res = int(op_args[0] == op_args[1])
        
    return [(packet_version_sum, res)]

def handle_length_packet(packet_type, packet_version, input):
    total_length = int(input[:15], 2)
    segment = input[15:15 + total_length]

    remaining = segment
    acc = [(packet_version, packet_type)]
    while(len(remaining) > 0):
        packet, remaining = get_next_packet(remaining)
        acc += packet
    return do_reduce(acc, packet_type), input[15 + total_length:]

def handle_num_packet(packet_type, packet_version, input):
    num_sub_packets = int(input[:11], 2)

    num_fetched = 0
    acc = [(packet_version, packet_type)]

    remaining = input[11:]
    while num_fetched < num_sub_packets:
        packet, remaining = get_next_packet(remaining)
        acc += packet
        num_fetched += 1

    return do_reduce(acc, packet_type), remaining

def get_next_packet(input):
    if set(input) == set(["0"]) or input == "":
        return [], ""

    packet_version = int(input[:3], 2)
    packet_type = int(input[3:6], 2)
    remaining = input[6:]

    if packet_type == 4:
        packet, remaining = handle_literal_packet(packet_version, remaining)
        return packet, remaining

    else:
        length_id = remaining[0]
        if length_id == "0":
            return handle_length_packet(packet_type, packet_version, remaining[1:])
        elif length_id == "1":
            return handle_num_packet(packet_type, packet_version, remaining[1:])

start = time.time()
initial = parse_input(input)
solve_acc, remaining = get_next_packet(initial)
answer1 = solve_acc[0][0]
answer2 = solve_acc[0][1]

print("Part 1")
print(f"Answer: {answer1}")
# print(submit(16, 1, answer1).text)

print("Part 2")
print(f"Answer: {answer2}")
# print(submit(16, 2, answer1).text)
print(f"Took {time.time() - start} seconds for both parts")