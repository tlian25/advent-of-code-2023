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
    curr = history
    stack = [curr[-1]]
    while not is_all_zero(curr):
        curr = generate_diffs(curr)
        stack.append(curr[-1])
    
    # walk back up stack
    while len(stack) > 1:
        diff = stack.pop()
        # extrapolate last value
        stack[-1] += diff
    
    return stack[0] 


def solution1():
    histories = parse_lines()
    
    res = 0
    for h in histories:
        v = derive_value_right(h)
        res += v

    return res
    
def derive_value_left(history:deque[int]) -> bool:
    curr = history
    stack = [curr[0]]
    while not is_all_zero(curr):
        curr = generate_diffs(curr)
        stack.append(curr[0])
    
    # walk back up stack
    while len(stack) > 1:
        diff = stack.pop()
        # extrapolate last value
        stack[-1] -= diff
    
    return stack[0] 


def solution2():
    histories = parse_lines()
    
    res = 0
    for h in histories:
        v = derive_value_left(h)
        res += v
    return res


if __name__ == '__main__':
    s = solution1()
    print("Part 1:", s) 
    assert s == 1987402313, s
    
    print('--------------')
    
    s = solution2()
    print("Part 2: ", s)
    assert s == 900, s