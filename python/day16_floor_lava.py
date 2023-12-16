# Day 16: The Floor Will Be Lava
# https://adventofcode.com/2023/day/16

from util.input_util import read_input_file
from collections import deque, defaultdict

def parse_lines():
    lines = read_input_file(16)
    grid = [list(l) for l in lines]
    return grid

def print_grid(grid, seen=set()):
    s = ''
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == SPACE and (r, c) in seen:
                s += '#'
            else:
                s += grid[r][c]
        s += '\n'
    print(s)
    

N = 'north'
S = 'south'
E = 'east'
W = 'west'

DIRS = {N: (-1,0), S: (1,0), E: (0,1), W: (0,-1)}

SLASH = '/'
BSLASH = '\\'
VERT = '|'
HORIZ = '-'
SPACE = '.'

SLASH_TRANSFORM = {N:E, E:N, S:W, W:S}
BLASH_TRANSFORM = {N:W, W:N, S:E, E:S}

def calc_next_dir(currdir, symbol) -> list:
    if symbol == SPACE: return [currdir]
    elif symbol == SLASH:
        return [SLASH_TRANSFORM[currdir]]
    elif symbol == BSLASH:
        return [BLASH_TRANSFORM[currdir]]
    elif symbol == HORIZ:
        if currdir in (E, W): return [currdir]
        else: return (E, W)
    elif symbol == VERT:
        if currdir in (N, S): return [currdir]
        else: return (N, S)
    raise ValueError("Unknown combo", currdir, symbol)
        
        

def bfs(r, c, d, grid):
    NR, NC = len(grid), len(grid[0])
    q = deque([(r, c, d)])
    seen = set()
    seen.add((0, 0, E))
    while q:
        r, c, d = q.popleft()
        s = grid[r][c]

        for nd in calc_next_dir(d, s):
            dr, dc = DIRS[nd]
            nr, nc = r+dr, c+dc
            if 0 <= nr < NR and 0 <= nc < NC:
                if (nr, nc, nd) not in seen:
                    seen.add((nr, nc, nd))
                    q.append((nr, nc, nd))
                    
    # unique seen by (r, c)
    unique_seen = set()
    for r, c, d in seen:
        unique_seen.add((r, c))
    return unique_seen
                

def solution1():
    grid = parse_lines()
    seen = bfs(0, 0, E, grid)
    return len(seen)
    
    
def solution2():
    grid = parse_lines()
    
    mxcount = 0
    for c in range(len(grid[0])):
        seen = bfs(0, c, S, grid)
        mxcount = max(mxcount, len(seen))

        seen = bfs(len(grid)-1, c, N, grid)
        mxcount = max(mxcount, len(seen))
    
    for r in range(len(grid)):
        seen = bfs(r, 0, E, grid)
        mxcount = max(mxcount, len(seen))
        
        seen = bfs(r, len(grid[0])-1, W, grid)
        mxcount = max(mxcount, len(seen))

    return mxcount
    
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())