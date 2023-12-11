# Day 11: Cosmic Expansion
# https://adventofcode.com/2023/day/11

from util.input_util import read_input_file
from collections import deque, defaultdict
from itertools import combinations

EMPTY = '.'
GALAXY = '#'
# Any rows or cols that contain no galaxies should be twice as big


def parse_lines():
    lines = read_input_file(11)
    grid = [list(l) for l in lines]
    return grid

def print_grid(grid, loop=[]):
    s = ''
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            p = grid[r][c]
            s += p
        s += '\n'
    s += '\n'
    print(s)

def emptyrowcols(grid) -> tuple:
    emptyrows = set()
    emptycols = set()
    for r in range(len(grid)):
        empty = True
        for c in range(len(grid)):
            if grid[r][c] == GALAXY:
                empty = False
                break
        if empty: emptyrows.add(r)
    
    for c in range(len(grid[0])):
        empty = True
        for r in range(len(grid)):
            if grid[r][c] == GALAXY:
                empty = False
                break
        if empty: emptycols.add(c)
    
    return emptyrows, emptycols



        
def find_galaxies(grid) -> set:
    galaxies = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == GALAXY:
                galaxies.add((r,c))
    return galaxies

def manhattan_dist(r1, c1, r2, c2, erows, ecols, multiplier) -> int:
    if r1 > r2: r1, r2 = r2, r1
    if c1 > c2: c1, c2 = c2, c1

    d = 0
    for r in range(r1+1, r2+1):
        if r in erows: d += multiplier
        else: d += 1
    
    for c in range(c1+1, c2+1):
        if c in ecols: d += multiplier
        else: d += 1
    
    return d

def calc_distances(galaxies, erows, ecols, multiplier) -> dict:
    dist = defaultdict(dict)
    for g1, g2 in combinations(galaxies, 2):
        dist[g1][g2] = manhattan_dist(*g1, *g2, erows, ecols, multiplier)
    return dist
        

def solution1():
    grid = parse_lines()
    erows, ecols = emptyrowcols(grid)

    galaxies = find_galaxies(grid)

    dists = calc_distances(galaxies, erows, ecols, 2)
    
    total_dist = 0
    for d1 in dists:
        for d2 in dists[d1]:
            total_dist += dists[d1][d2]
            # print(d1, d2, dists[d1][d2])
    
    return total_dist

    

    

    
    
def solution2():
    grid = parse_lines()
    erows, ecols = emptyrowcols(grid)

    galaxies = find_galaxies(grid)

    dists = calc_distances(galaxies, erows, ecols, 1_000_000)
    
    total_dist = 0
    for d1 in dists:
        for d2 in dists[d1]:
            total_dist += dists[d1][d2]
            # print(d1, d2, dists[d1][d2])
    
    return total_dist    
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())