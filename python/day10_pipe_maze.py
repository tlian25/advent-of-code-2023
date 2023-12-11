# Day 10: Pipe Maze
# https://adventofcode.com/2023/day/10

from util.input_util import read_input_file
from collections import deque, defaultdict

def parse_lines():
    lines = read_input_file(10)
    grid = [list(l) for l in lines]
    return grid

def print_grid(grid, loop=[]):
    s = ''
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            p = grid[r][c]
            if (r, c) in loop:
                s += '+'
            else:
                s += p
        s += '\n'
    s += '\n'
    print(s)


def print_shrinked_grid(expandgrid, loop=[]):
    s = ''
    for r in range(0, len(expandgrid), 3):
        for c in range(0, len(expandgrid[0]), 3):
            p = expandgrid[r][c]
            if (r, c) in loop:
                s += '+'
            elif p in (INSIDE, OUTSIDE):
                s += p
            else:
                s += ' '
        s += '\n'
    s += '\n'
    print(s)


NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'

# Pipe types
NS = '|'
EW = '-'
NE = 'L'
NW = 'J'
SW = '7'
SE = 'F'
GROUND = '.'
START = 'S'

DIRS = {NORTH: (-1,0), SOUTH: (1,0), EAST: (0,1), WEST: (0,-1)}
OPDIR = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}

INSIDE = 'I'
OUTSIDE = 'O'
OTHER = '+'

def get_dirs_for_pipe(pipetype) -> tuple:
    if pipetype == NS: return NORTH, SOUTH
    if pipetype == NE: return NORTH, EAST
    if pipetype == NW: return NORTH, WEST 
    if pipetype == SE: return SOUTH, EAST
    if pipetype == SW: return SOUTH, WEST
    if pipetype == EW: return EAST, WEST
    if pipetype == START: return NORTH, SOUTH, EAST, WEST
    raise ValueError(f"Unknown pipetype: {pipetype}")


def is_connected(dir, r, c, grid) -> bool:
    return dir in get_dirs_for_pipe(grid[r][c])


def find_start(grid) -> tuple:
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == START: return r, c
    return -1, -1


def bfs(r, c, grid) -> dict:
    NR, NC = len(grid), len(grid[0])
    # return a dict of d[(r, c)] = steps from start
    q = deque([(r, c, 0)])
    d = {(r,c): 0}
    while q:
        r, c, steps = q.popleft()
        pipe = grid[r][c]

        for dir in get_dirs_for_pipe(pipe):
            dr, dc = DIRS[dir]
            nr, nc = r+dr, c+dc
            if 0 <= nr < NR and 0 <= nc < NC and (nr, nc) not in d:
                if grid[nr][nc] != GROUND and is_connected(OPDIR[dir], nr, nc, grid):
                    d[(nr, nc)] = steps+1
                    q.append((nr, nc, steps+1))
    return d

def bfs_onedirection(r, c, grid) -> list:
    NR, NC = len(grid), len(grid[0])
    # return a dict of d[(r, c)] = steps from start
    q = deque([(r, c, 0)])
    seen = set([(r,c)])
    order = []
    while q:
        r, c, steps = q.popleft()
        pipe = grid[r][c]
        order.append((r, c))

        for dir in get_dirs_for_pipe(pipe):
            dr, dc = DIRS[dir]
            nr, nc = r+dr, c+dc
            if 0 <= nr < NR and 0 <= nc < NC and (nr, nc) not in seen:
                if grid[nr][nc] != GROUND and is_connected(OPDIR[dir], nr, nc, grid):
                    seen.add((nr, nc))
                    q.append((nr, nc, steps+1))
                    break
    return order


def floodfill(r, c, grid, loop) -> int:
    NR, NC = len(grid), len(grid[0])
    # flood as either INSIDE, or OUTSIDE
    # if we eventually hit outside then it's outside of the loop
    # otherwise inside the loop
    outside = False
    q = deque([(r, c)])
    seen = set([(r,c)])
    while q:
        r, c, = q.popleft()
        if r in (0, NR-1) or c in (0, NC-1): outside = True
        
        for dr, dc in DIRS.values():
            nr, nc = r+dr, c+dc
            if 0<=nr<NR and 0<=nc<NC and (nr, nc) not in loop and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append((nr, nc))
    
    marking = OUTSIDE if outside else INSIDE

    count = 0
    for r, c in seen:
        if grid[r][c] != ' ':
            count += 1
        grid[r][c] = marking
        
    
    if outside: return 0
    return count
        


def oddIntersections(r, c, grid, loop) -> bool:
    intersects = 0
    for x in range(r):
        if (x, c) in loop or grid[x][c] == '*':
            intersects += 1
    
    return intersects % 2 == 1
        



def connect_pipes(r1, c1, r2, c2, grid, loop):
    if r1 > r2: r1, r2 = r2, r1
    if c1 > c2: c1, c2 = c2, c1

    if c1 == c2:
        for r in range(r1+1, r2):
            grid[r][c1] = '*'
            loop.add((r, c1))
    elif r1 == r2:
        for c in range(c1+1, c2):
            grid[r1][c] = '*'
            loop.add((r1, c))
    else:
        raise ValueError("Unknown case")


def expand_grid(grid, order):
    expandgrid = [[' ' for _ in range(len(grid[0])*3)] for _ in range(len(grid)*3)]
    expandloop = set()

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            expandgrid[r*3][c*3] = grid[r][c]

    # Connect grid in order
    for i in range(len(order)-1):
        r1, c1 = order[i]
        r2, c2 = order[i+1]
        expandloop.add((r1*3, c1*3))
        expandloop.add((r2*3, c2*3))
        connect_pipes(r1*3, c1*3, r2*3, c2*3, expandgrid, expandloop)
    
    # connect first and last
    r1, c1 = order[0]
    r2, c2 = order[-1]
    connect_pipes(r1*3, c1*3, r2*3, c2*3, expandgrid, expandloop)

    return expandgrid, expandloop
        




def solution1():
    grid = parse_lines() 
    # find start
    r0, c0 = find_start(grid)
    steps = bfs(r0, c0, grid)
    return max(steps.values())



def solution2():
    grid = parse_lines() 
    # find start
    r0, c0 = find_start(grid)
    order = bfs_onedirection(r0, c0, grid)
    
    expandgrid, expandloop = expand_grid(grid, order)

    count = 0
    for r in range(len(expandgrid)):
        for c in range(len(expandgrid[0])):
            if (r, c) not in expandloop and expandgrid[r][c] not in (INSIDE, OUTSIDE):
                count += floodfill(r, c, expandgrid, expandloop)
                    
    # print_shrinked_grid(expandgrid, expandloop)
    return count




if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())