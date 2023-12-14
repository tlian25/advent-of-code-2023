# Day 14: Parabolic Reflector Dish
# https://adventofcode.com/2023/day/14

from util.input_util import read_input_file
from collections import deque, defaultdict
from tqdm import tqdm
from functools import cache
from copy import deepcopy

NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'

CUBE_ROCK = '#'
ROUND_ROCK = 'O'
EMPTY = '.'
DIR = {NORTH: (-1,0), SOUTH: (1,0), EAST: (0,1), WEST: (0,-1)}

class Dish:
    def __init__(self, grid):
        self.grid = grid
        self.original_grid = deepcopy(grid)
        self.NR = len(grid)
        self.NC = len(grid[0])
    
    def tilt_north(self):
        # move each round rock as far north as it will go
        for r in range(1, self.NR):
            for c in range(self.NC):
                if self.grid[r][c] == ROUND_ROCK:
                    self.move_round_rock(r, c, NORTH)
                    
    def tilt_south(self):
        for r in range(self.NR-2, -1, -1):
            for c in range(self.NC):
                if self.grid[r][c] == ROUND_ROCK:
                    self.move_round_rock(r, c, SOUTH)
    
    def tilt_east(self):
        for c in range(self.NC-2, -1, -1):
            for r in range(self.NR):
                if self.grid[r][c] == ROUND_ROCK:
                    self.move_round_rock(r, c, EAST)
                
    def tilt_west(self):
        for c in range(1, self.NC):
            for r in range(self.NR):
                if self.grid[r][c] == ROUND_ROCK:
                    self.move_round_rock(r, c, WEST)
                
    def cycle_all_dirs(self):
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()
    
    def move_round_rock(self, r, c, dir):
        dr, dc = DIR[dir]
        nr, nc = r+dr, c+dc
        while 0<=nr<self.NR and 0<=nc<self.NC and self.grid[nr][nc] == EMPTY:
            self.grid[nr][nc] = ROUND_ROCK
            self.grid[r][c] = EMPTY
            r, c = nr, nc
            nr, nc = nr+dr, nc+dc
    
        
    def calc_load_north(self) -> int:
        load = 0
        for r in range(self.NR):
            n = self.grid[r].count(ROUND_ROCK)
            load += n * (self.NR - r)
        return load
    
    def reset_grid(self):
        self.grid = deepcopy(self.original_grid)

    def __repr__(self):
        s = ''
        for row in self.grid:
            s += ''.join(row) + '\n'
        return s

    def __hash__(self):
        return hash(self.__repr__())

        

def parse_lines():
    lines = read_input_file(14)
    grid = [list(l) for l in lines]
    dish = Dish(grid)
    return dish





def solution1():
    dish = parse_lines()
    dish.tilt_north()
    return dish.calc_load_north()
    
    
def solution2():
    dish = parse_lines()
    cycles = 1_000_000_000
    seen = {str(dish): 0}

    for c in range(1, cycles+1):
        dish.cycle_all_dirs()
        if str(dish) in seen:
            last_seen = seen[str(dish)]
            curr_seen = c
            break
        else:
            seen[str(dish)] = c

    # Calculate how many more times we need to cycle in directions after
    # Advancing and skipping cycles of seen states
    remain = (cycles - last_seen) % (curr_seen - last_seen)

    for r in range(remain):
        dish.cycle_all_dirs()
    
    # print(dish)
    return dish.calc_load_north()
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())