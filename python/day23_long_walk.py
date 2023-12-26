# Day 23: A Long Walk
# https://adventofcode.com/2023/day/23

from util.input_util import read_input_file
from collections import deque, defaultdict
from heapq import heappop, heappush

PATH = '.'
FOREST = '#'
NSLOPE = '^'
ESLOPE = '>'
WSLOPE = '<'
SSLOPE = 'v'

DIR = [(1, 0), (0, 1), (-1, 0), (0, -1)]
SDIR = {NSLOPE: (-1, 0), SSLOPE: (1, 0), ESLOPE: (0, 1), WSLOPE: (1, 0)}

def parse_lines():
    lines = read_input_file(23)
    grid = [list(l) for l in lines]
    return grid

def print_grid(grid, seen=set()):
    s = ''
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) in seen:
                s += 'O'
            elif grid[r][c] == FOREST:
                s += FOREST
            else:
                s += PATH
        s += '\n'
    s += '\n'
    print(s)

def find_start_end(grid):
    for c in range(len(grid[0])):
        if grid[0][c] == PATH:
            start = (0, c)
        if grid[-1][c] == PATH:
            end = (len(grid)-1, c)
    return start, end


def bfs(grid):
    NR, NC = len(grid), len(grid[0])
    start, end = find_start_end(grid)
    r0, c0 = start
    r1, c1 = end
    seen = set([(r0, c0)])
    q = deque([(r0, c0, seen)])
    maxseen = set()
    while q:
        r, c, seen = q.popleft()
        if r == r1 and c == c1:
            if len(seen) > len(maxseen):
                maxseen = seen
            continue

        if grid[r][c] in SDIR:
            dr, dc = SDIR[grid[r][c]]
            nr, nc = r+dr, c+dc
            if (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append((nr, nc, seen))
            continue
            
        for dr, dc in DIR:
            nr, nc = r+dr, c+dc
            if 0 <= nr < NR and 0 <= nc < NC and (nr, nc) not in seen and grid[nr][nc] != FOREST:
                seencopy = seen.copy()
                seencopy.add((nr, nc))
                q.append((nr, nc, seencopy))
        
    return maxseen

def zero_grid(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != FOREST:
                grid[r][c] = 0


def build_graph(grid):
    NR, NC = len(grid), len(grid[0])
    start, end = find_start_end(grid)
    r0, c0 = start
    graph = defaultdict(dict)
    curr = r0+1, c0
    # x, y, prev, last_node, visited, steps
    q = deque([(curr, start, start, set([start]), 1)])
    while q:
        curr, prev, last_node, visited, steps = q.popleft()
        r, c = curr

        if curr == end:
            graph[last_node][curr] = steps
            graph[curr][last_node] = steps
            continue

        nbs = []
        for dr, dc in DIR:
            nr, nc = r+dr, c+dc
            if 0 <= nr < NR and 0 <= nc < NC and grid[nr][nc] != FOREST:
                if (nr, nc) != prev:
                    nbs.append((nr, nc))
        
        if len(nbs) == 1:
            nr, nc = nbs[0]
            visited.add((nr, nc))
            q.append((nbs[0], curr, last_node, visited, steps+1))
            continue
        
        if curr in graph[last_node]: continue
        # Mark curr as a node in graph
        graph[last_node][curr] = steps
        graph[curr][last_node] = steps
        last_node = curr
        prev = curr
        for nr, nc in nbs:
            curr = (nr, nc)
            q.append((curr, prev, last_node, set([prev]), 1))

    return graph



def bfs_graph(graph, grid):
    start, end = find_start_end(grid)
    q = deque([(start, 0, set([start]))])
    mxsteps = 0
    while q:
        curr, steps, visited = q.popleft()
        if curr == end:
            mxsteps = max(mxsteps, steps)
            continue

        for nb in graph[curr]:
            if nb not in visited:
                copyvisited = visited.copy()
                copyvisited.add(nb)
                q.append((nb, steps + graph[curr][nb], copyvisited))
    
    return mxsteps


def dfs_graph(node, end, graph, seen, steps):
    if node == end:
        return steps
    
    mxsteps = 0
    for nb in graph[node]:
        if nb not in seen:
            seen.add(nb)
            s = dfs_graph(nb, end, graph, seen, steps+graph[node][nb])
            mxsteps = max(mxsteps, s)
            seen.remove(nb)
    
    return mxsteps

    




def solution1():
    grid = parse_lines()
    maxseen = bfs(grid)
    return len(maxseen)-1

def solution2():
    grid = parse_lines()
    graph = build_graph(grid)
    start, end = find_start_end(grid)
    
    # DFS much faster than BFS
    return dfs_graph(start, end, graph, {start}, 0)
    # return bfs_graph(graph, grid)
    
    
    
    
if __name__ == '__main__':
    # print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())