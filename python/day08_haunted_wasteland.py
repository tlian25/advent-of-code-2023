# Day 8: Haunted Wasteland
# https://adventofcode.com/2023/day/8

from util.input_util import read_input_file
from collections import deque, defaultdict
import math

LEFT = 0
RIGHT = 1

def parse_lines():
    lines = read_input_file(8)
    dirs = [d == 'R' for d in list(lines[0])]
    graph = {}
    nodes = set()
    for l in lines[2:]:
        n, lr = l.split(' = ')
        l, r = lr.split(', ')
        l = l.replace('(', '')
        r = r.replace(')', '')
        nodes.add(n)
        nodes.add(l)
        nodes.add(r)
        graph[n] = (l, r)
    
    return dirs, nodes, graph
    

def solution1():
    dirs, nodes, graph = parse_lines()
    MOD = len(dirs)

    steps = 0
    currnode = 'AAA'
    while True:
        if currnode == 'ZZZ': return steps
        
        d = dirs[steps % MOD]
        currnode = graph[currnode][d]
        steps += 1


def solution2():
    dirs, nodes, graph = parse_lines()
    MOD = len(dirs)
    

    startnodes = [n for n in nodes if n[2] == 'A']
    currnodes = startnodes.copy()
    
    LSTARTNODES = len(startnodes)
    cycle = {}
    steps = 0
    while True:
        # Found cycle for all nodes
        if len(cycle) == LSTARTNODES:
            return math.lcm(*cycle.values())

        d = dirs[steps % MOD]
        for i, c in enumerate(currnodes):
            if i in cycle:
                pass
            elif c[2] == 'Z': # end
                cycle[i] = steps
            else:
                currnodes[i] = graph[c][d]
        
        steps += 1

 

if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())