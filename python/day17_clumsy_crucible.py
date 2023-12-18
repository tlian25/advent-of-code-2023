# Day 17: Clumsy Crucible
# https://adventofcode.com/2023/day/17

from util.input_util import read_input_file
from collections import deque, defaultdict
from heapq import heappush, heappop

def parse_lines():
    lines = read_input_file(17)
    grid = [[int(x) for x in l] for l in lines]
    return grid

# Can move at most three blocks in a single direction before it must turn
# Cannot reverse - only left, right, or straight

N, S, E, W = 'N', 'S', 'E', 'W'
DIR = {N:(-1,0), S:(1,0), E:(0,1), W:(0,-1)}

def turn_left(currdir):
    if currdir == N: return W
    if currdir == W: return S
    if currdir == S: return E
    if currdir == E: return N

def turn_right(currdir):
    if currdir == N: return E
    if currdir == E: return S
    if currdir == S: return W
    if currdir == W: return N

def bfs(grid, minstep, maxstep):
    NR, NC = len(grid), len(grid[0])
    dp = defaultdict(int)
    dp[(0, 0, E, 0)] = 0

    q = [(0, 0, 0, E, 0)]
    while q:
        h, r, c, d, s = heappop(q)
        print('\r', r, c, d, s, h, end='')

        if r == NR-1 and c == NC-1:
            continue

        if s < maxstep: # can continue in same direction
            dr, dc = DIR[d]
            nr, nc = r+dr, c+dc
            if 0 <= nr < NR and 0 <= nc < NC:
                nh = h + grid[nr][nc]
                if (nr, nc, d, s+1) not in dp or nh < dp[(nr, nc, d, s+1)]:
                    dp[(nr, nc, d, s+1)] = nh
                    heappush(q, (nh, nr, nc, d, s+1))
        
        # turn left and right
        if minstep <= s:
            for nd in (turn_left(d), turn_right(d)):
                dr, dc = DIR[nd]
                nr, nc = r+dr, c+dc
                if 0 <= nr < NR and 0 <= nc < NC:
                    nh = h + grid[nr][nc]
                    if (nr, nc, nd, 1) not in dp or nh < dp[(nr, nc, nd, 1)]:
                        dp[(nr, nc, nd, 1)] = nh
                        heappush(q, (nh, nr, nc, nd, 1))

    print()
    minh = float('inf')
    for r, c, d, s in dp:
        if r == NR-1 and c == NC-1 and s >= minstep:
            m = dp[(r,c,d,s)]
            minh = min(minh, m)
    return minh



def solution1():
    grid = parse_lines()
    m = bfs(grid, 0, 3)
    return m
    
    
def solution2():
    grid = parse_lines()
    m = bfs(grid, 4, 10)
    return m
    
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())