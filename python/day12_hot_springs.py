# Day 12: Hot Springs
# https://adventofcode.com/2023/day/12

from util.input_util import read_input_file
from collections import deque, defaultdict
import re
from functools import cache

OPERATIONAL = '.'
DAMAGED = '#'
WILDCARD = '?'

def parse_lines():
    lines = read_input_file(12)
    patterns = []
    records = []
    for l in lines:
        p, r = l.split()
        patterns.append(list(p))
        records.append([int(x) for x in r.split(',')])
    
    return patterns, records


@cache
def match(p, symbol):
    s = set(p)
    if symbol == DAMAGED:
        res = OPERATIONAL not in s
    else:
        res = DAMAGED not in s
    return res


def possible_ways(pattern:str, record:list):
    # Need to implement some sort of Dynamic programming
    L = len(pattern)

    REMAIN = L - sum(record)
    # DFS_CACHE = {}
    
    @cache
    def dfs(i, remain, l):
        if pattern[l] == OPERATIONAL:
            return 0

        if remain <= 0 and i < len(record)-1:
            return 0

        if L - l - remain - sum(record[i:]) < 0:
            return 0
    
        if not match(pattern[l:l+record[i]], DAMAGED):
            return 0
        
        l += record[i]

        if i == len(record)-1: # last record used
            if match(pattern[l:], OPERATIONAL):
                return 1
            return 0

        w = 0
        for r in range(1, remain+1):
            if pattern[l+r-1] == DAMAGED:
                break
            w += dfs(i+1, remain - r, l + r)

        return w
    
    # front prefix for all possible fillers
    ways = 0
    for r in range(REMAIN+1):
        if r == 0 or pattern[r-1] != DAMAGED:
            ways += dfs(0, REMAIN-r, r)
        else:
            break
            
    return ways


def possible_ways2(pattern, record):
    # In-place DFS
    L = len(pattern)
    REMAIN = L - sum(record)
    DFS_CACHE = {}

    stack = []
    for r in range(REMAIN+1):
        if r == 0 or pattern[r-1] != DAMAGED:
            stack.append((0, REMAIN-r, r))


    
    
    
    
        

def unfold(pattern, record, n):
    pattern = (pattern + [WILDCARD]) * (n-1) + pattern
    record *= n
    return pattern, record


def solution1():
    patterns, records = parse_lines()
    
    totalways = 0
    for p, r in zip(patterns, records):
        ways = possible_ways(''.join(p), r)
        # ways = possible_ways(p, r)
        totalways += ways
    return totalways
        
    
    
def solution2():
    patterns, records = parse_lines()
    
    totalways = 0
    n = 5
    i = 0
    for p, r in zip(patterns, records):
        p, r = unfold(p, r, n)
        ways = possible_ways(''.join(p), r)
        totalways += ways
        i += 1
        
    return totalways
    
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())