# Day 2: Cube Conundrum
# https://adventofcode.com/2023/day/2

from typing import List
from util.input_util import read_input_file

class Game:
    def __init__(self, num:int, subgames:List[dict]):
        self.num = num
        self.subgames = subgames
    
    def hasNextSubgame(self):
        return len(self.subgames) > 0

    def getNextSubgame(self):
        return self.subgames.pop()
    
RED = "red"
BLUE = "blue"
GREEN = "green"
    
def parse_subgames(subgames:str) -> List[dict]:
    sgs = []
    for s in subgames.split("; "):
        # 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        sg = {}
        for c in s.split(', '):
            # 3 blue
            n, c =  c.split(' ')
            sg[c] = int(n)
        sgs.append(sg)

    return sgs
            

def parse_lines():
    lines = read_input_file(2)
    games = []
    for l in lines:
        game, subgames = l.split(": ")
        g = Game(int(game.split()[1]), parse_subgames(subgames))
        games.append(g)

    return games
        

def isPossible(subgame, cubes):
    for c, n in subgame.items():
        if c in cubes and cubes[c] >= n:
            continue
        return False
    return True


def solution1():
    games = parse_lines()
    res = 0

    CUBES = {RED: 12, GREEN: 13, BLUE: 14}
    for g in games:
        possible = True
        while possible and g.hasNextSubgame():
            sg = g.getNextSubgame()
            possible = isPossible(sg, CUBES)
        
        if possible: res += g.num
    return res

    
def updateMaxCubes(subgame, maxCubes):
    for c, n in subgame.items():
        maxCubes[c] = max(maxCubes[c], n)

    
def solution2():
    games = parse_lines()
    res = 0

    for g in games:
        maxCubes = {RED: 0, GREEN: 0, BLUE: 0}
        while g.hasNextSubgame():
            updateMaxCubes(g.getNextSubgame(), maxCubes)

        prod = 1
        for _, n in maxCubes.items():
            prod *= n
        res += prod
    
    return res
    
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())