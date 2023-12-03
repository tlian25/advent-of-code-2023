# Day 3: Gear Ratios
# https://adventofcode.com/2023/day/3

from util.input_util import read_input_file
from collections import defaultdict

SPACE = '.'
GEAR = '*'

def parse_lines():
    lines = read_input_file(3)
    grid = []
    for l in lines:
        grid.append(list(l) + [SPACE])
    return grid


def is_digit(char):
    return '0' <= char <= '9'

def is_symbol(char):
    return char != SPACE and not is_digit(char)


def extract_numbers(grid):
    # return tuple of (num, r, c) where num starts at r, c
    nums = []
    rr, cc = None, None
    n = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if is_digit(grid[r][c]):
                if not n:
                    rr = r
                    cc = c
                n.append(grid[r][c])
            elif n:
                # append num and reset
                nums.append((int(''.join(n)), rr, cc))
                n = []
                rr, cc = None, None
    return nums


def adjacent_symbol(r, c, grid):
    while (is_digit(grid[r][c])):
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                if is_symbol(grid[nr][nc]):
                    return True
        c+=1
    return False
        


def extract_parts(nums, grid):
    parts = []
    for n, r, c in nums:
        if adjacent_symbol(r, c, grid):
            parts.append(n)
    return parts
    


def solution1():
    grid = parse_lines() 
    nums = extract_numbers(grid)
    parts = extract_parts(nums, grid)
    return sum(parts)


def adjacent_gear(r, c, grid):
    while (is_digit(grid[r][c])):
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                if grid[nr][nc] == GEAR:
                    return nr, nc
        c+=1
    return -1, -1 
    
def extract_gear_ratios(nums, grid):
    gear_ratios = defaultdict(list)

    for n, r, c in nums:
        gr, gc = adjacent_gear(r, c, grid)
        if gr != -1:
            gear_ratios[(gr, gc)].append(n)
    
    return gear_ratios
            
        

    
def solution2():
    grid = parse_lines()
    nums = extract_numbers(grid)
    gear_ratios = extract_gear_ratios(nums, grid)

    
    res = 0
    for g, l in gear_ratios.items():
        if len(l) == 2:
            res += l[0] * l[1]
    
    return res
            
    
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())