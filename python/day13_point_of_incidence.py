# Day 13: Point of Incidence
# https://adventofcode.com/2023/day/13

from util.input_util import read_input_file
from collections import deque, defaultdict

ASH = '.'
ROCK = '#'

def parse_lines():
    lines = read_input_file(13)
    patterns = []
    p = []
    for l in lines:
        if l == "":
            patterns.append(p)
            p = []
        else:
            p.append(list(l))

    patterns.append(p)
    return patterns

def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print()


def expand_col(r, c, grid) -> int:
    row = grid[r]
    i, j = c, c+1
    diffs = 0
    while i >= 0 and j < len(row):
        if row[i] != row[j]:
            diffs += 1
        i -= 1
        j += 1
    return diffs 


def expand_row(r, c, grid) -> int:
    col = [grid[rr][c] for rr in range(len(grid))]
    i, j = r, r+1
    diffs = 0
    while i >= 0 and j < len(col):
        if col[i] != col[j]:
            diffs += 1
        i -= 1
        j += 1
    return diffs 

# For Part 1 - exact match
def find_mirror_col(grid) -> int:
    for c in range(len(grid[0])-1):
        valid = True
        for r in range(len(grid)):
            if expand_col(r, c, grid) != 0:
               valid = False 
               break
        if valid: return c
    return -1


def find_mirror_row(grid) -> int:
    for r in range(len(grid)-1):
        valid = True 
        for c in range(len(grid[0])):
            if expand_row(r, c, grid) != 0:
                valid = False
                break
        if valid: return r
    return -1


# For Part 2 - allow one fix/diff
def find_mirror_col_diff(grid) -> int:
    for c in range(len(grid[0])-1):
        diffs = 0
        for r in range(len(grid)):
            diffs += expand_col(r, c, grid)
            if diffs > 1:
               break
        if diffs == 1: return c
    return -1

def find_mirror_row_diff(grid) -> int:
    for r in range(len(grid)-1):
        diffs = 0
        for c in range(len(grid[0])):
            diffs += expand_row(r, c, grid)
            if diffs > 1:
                break
        if diffs == 1: return r
    return -1 

def solution1():
    patterns = parse_lines()

    res = 0
    for p in patterns:
        r, c = None, None
        r = find_mirror_row(p)
        c = find_mirror_col(p)

        if c == -1 and r == -1:
            print_grid(p)
            raise ValueError("Neither row nor col found")
        if c != -1 and r != -1:
            print_grid(p)
            print(r, c)
            raise ValueError("Both row and col found")
        
        if r != -1:
            res += (r+1) * 100
        if c != -1:
            res += (c+1)

    return res


def solution2():
    patterns = parse_lines()

    res = 0
    for p in patterns:
        r, c = None, None
        r = find_mirror_row_diff(p)
        c = find_mirror_col_diff(p)

        if c == -1 and r == -1:
            print_grid(p)
            raise ValueError("Neither row nor col found")
        if c != -1 and r != -1:
            print_grid(p)
            print(r, c)
            raise ValueError("Both row and col found")
        
        if r != -1:
            res += (r+1) * 100
        if c != -1:
            res += (c+1)

    return res
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())