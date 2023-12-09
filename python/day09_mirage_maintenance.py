# Day 9: Mirage Maintanence
# https://adventofcode.com/2023/day/9

from util.input_util import read_input_file
from collections import deque, defaultdict
from typing import List

def parse_lines() -> List[deque]:
    lines = read_input_file(9)
    histories = []
    for l in lines:
        histories.append(deque([int(x) for x in l.split()]))
    return histories

# each line contains the history of a single value
# report should include a prediction of the next value
# 1. make new sequence from diff at each step
# 2. if seq not all zeros, repeat the process using generated seq as input

def is_all_zero(history:deque[int]) -> bool:
    return all([x == 0 for x in history])

def generate_diffs(history:deque[int]) -> deque[int]:
    diffs = deque()
    for i in range(1, len(history)):
        diffs.append(history[i]- history[i-1])
    return diffs


def derive_value_right(history:deque[int]) -> bool:
    stack = [history]
    while not is_all_zero(stack[-1]):
        curr = stack[-1]
        diffs = generate_diffs(curr)
        stack.append(diffs)
    
    # walk back up stack
    val = None
    while len(stack) > 1:
        diff = stack.pop()
        # extrapolate last value
        val = stack[-1][-1] + diff[-1]
        stack[-1].append(val)
    
    return val


def solution1():
    histories = parse_lines()
    
    res = 0
    for h in histories:
        v = derive_value_right(h)
        res += v

    return res
    
def derive_value_left(history:deque[int]) -> bool:
    stack = [history]
    while not is_all_zero(stack[-1]):
        curr = stack[-1]
        diffs = generate_diffs(curr)
        stack.append(diffs)
    
    # walk back up stack
    val = None
    while len(stack) > 1:
        diff = stack.pop()
        # extrapolate last value
        val = stack[-1][0] - diff[0]
        stack[-1].appendleft(val)
    
    return val


def solution2():
    histories = parse_lines()
    
    res = 0
    for h in histories:
        v = derive_value_left(h)
        res += v
    return res


if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())