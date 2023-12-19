# Day 18: Lavaduct Lagoon
# https://adventofcode.com/2023/day/18

from util.input_util import read_input_file
from collections import deque, defaultdict

def parse_lines():
    lines = read_input_file(18)
    instructions = []
    for l in lines:
        d, s, c = l.split()
        instructions.append((d, int(s), c))
    return instructions

U = 'U'
D = 'D'
R = 'R'
L = 'L'
TRENCH = '#'
GROUND = '.'
DIR = {U:(-1,0), D:(1,0), R:(0,1), L:(0,-1)}

def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print()

### Part 1
def dig(instructions):
    g = set([(0, 0)])
    minr, maxr, minc, maxc = 0, 0, 0, 0
    r = 0
    c = 0
    for d, s, _ in instructions:
        dr, dc = DIR[d]
        for _ in range(s):
            r, c = r+dr, c+dc
            minr = min(minr, r)
            maxr = max(maxr, r)
            minc = min(minc, c)
            maxc = max(maxc, c)
            g.add((r,c))
    
    # create grid
    grid = []
    for r in range(minr, maxr+1):
        row = []
        for c in range(minc, maxc+1):
            if (r, c) in g:
                row.append(TRENCH)
            else:
                row.append(GROUND)
        grid.append(row)
    return grid

def intersections(r, c, grid):
    count = 0
    for i in range(r):
        if grid[i][c] == TRENCH:
            count += 1
    return count

def flood_fill(r, c, grid):
    NR, NC = len(grid), len(grid[0])
    q = deque([(r,c)])
    grid[r][c] = TRENCH
    while q:
        r, c = q.popleft()
        for dr, dc in DIR.values():
            nr, nc = r+dr, c+dc
            if 0 <= nr < NR and 0 <= nc < NC:
                if grid[nr][nc] == GROUND:
                    grid[nr][nc] = TRENCH
                    q.append((nr, nc))

def fill_inside(grid):
    # Find a starting block on the inside
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == GROUND:
                count = intersections(r, c, grid)
                if count % 2 == 1: #inside
                    flood_fill(r, c, grid)
                    return
    
def count_trenches(grid):
    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == TRENCH:
                count += 1
    return count

#### Part 2

def digit_to_dir(d):
    if d == '0': return R
    if d == '1': return D
    if d == '2': return L
    if d == '3': return U
    raise ValueError(f'Unknown direction: {d}')

def dighex(instructions):
    vertices = [(0, 0)]
    r = 0
    c = 0
    perimeter = 0
    for i, (_, _, hex) in enumerate(instructions):
        s, d = int(hex[2:7], 16), digit_to_dir(hex[7])
        print('\r', i, s, d, end='')
        dr, dc = DIR[d]
        for _ in range(s):
            r, c = r+dr, c+dc
            perimeter += 1
        vertices.append((r,c))
    print()
    return vertices, perimeter

# https://artofproblemsolving.com/wiki/index.php/Shoelace_Theorem
def shoelace_area(vertices):
    s = 0
    for i in range(len(vertices)-1):
        x1, y1 = vertices[i]
        x2, y2 = vertices[i+1]
        s += x1*y2 - y1*x2
    
    return abs(s) // 2



def solution1():
    instructions = parse_lines()
    grid = dig(instructions)
    
    fill_inside(grid)
    count = count_trenches(grid)
    return count
    

def solution2():
    instructions = parse_lines()
    vertices, perimeter = dighex(instructions)
    totalarea = shoelace_area(vertices) + perimeter // 2 + 1
    return totalarea
    
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())