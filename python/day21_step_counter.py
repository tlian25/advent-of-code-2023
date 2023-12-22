# Day 21: Step Counter
# https://adventofcode.com/2023/day/21

from util.input_util import read_input_file
from collections import deque, defaultdict

GARDEN = '.'
ROCK = '#'
START = 'S'

DIRS = [(1,0), (0,1), (-1,0), (0,-1)]

def parse_lines():
    lines = read_input_file(21)
    grid = [list(l) for l in lines]
    return grid


def find_start(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == START:
                return r, c

def bfs(grid, steps):
    NR, NC = len(grid), len(grid[0])
    r0, c0 = find_start(grid)
    q = deque([(r0, c0, 0)])
    seen = set()
    ends = set()
    while q:
        r, c, s = q.popleft()
        if s % 2 == steps % 2:
            ends.add((r, c))
        
        if s == steps:
            continue

        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0 <= nr < NR and 0 <= nc < NC and grid[nr][nc] != ROCK:
                if (nr, nc) not in seen:
                    seen.add((nr, nc))
                    q.append((nr, nc, s+1))
    return ends


def bfs2(grid, steps):
    NR, NC = len(grid), len(grid[0])
    r0, c0 = find_start(grid)
    q = deque([(r0, c0, 0)])
    seen = set()
    ends = set()
    while q:
        r, c, s = q.popleft()
        print('\r', s, end='')
        if s % 2 == steps % 2:
            ends.add((r, c))
        
        if s == steps:
            continue

        for dr, dc in DIRS:
            # Extend in every direction
            nr, nc = r+dr, c+dc
            if grid[nr % NR][nc % NC] != ROCK:
                if (nr, nc) not in seen:
                    seen.add((nr, nc))
                    q.append((nr, nc, s+1))
    print()
    return ends
        


def solution1():
    grid = parse_lines()
    ends = bfs(grid, 64)
    return len(ends)
    
    
def solution2():
    grid = parse_lines()

    # 26501365 = 202300 * 131 + 65
    # 131 is side length of input grid
    ends = bfs2(grid, 65)
    r1 = len(ends)

    ends = bfs2(grid, 65 + 131)
    r2 = len(ends)

    ends = bfs2(grid, 65 + 131 * 2)
    r3 = len(ends)
    
    print(r1, r2, r3)
    # solve polynomial

    a = (r3 + r1 - 2 * r2) // 2
    b = (4 * r2 - 3 * r1 - r3) // 2
    c = r1
    print(a, b, c)

    x = 202300
    return a * x ** 2 + b * x + c
    
    
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())