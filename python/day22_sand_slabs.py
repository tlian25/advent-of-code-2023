# Day 22: Sand Slabs
# https://adventofcode.com/2023/day/22

from util.input_util import read_input_file
from collections import deque, defaultdict

SPACE = '.'
BRICK = '#'

class Brick:
    def __init__(self, name, x0, y0, z0, x1, y1, z1):
        self.name = name
        self.ends = [z0, x0, y0, z1, x1, y1]
        self.positions = []
        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                for z in range(z0, z1+1):
                    self.positions.append((z, x, y))
        self.positions.sort()
        self.ontopoff = None
    
    def get_positions(self):
        return self.positions
    
    def get_name(self):
        return self.name
    
    def __lt__(self, other):
        return self.ends < other.ends
        
    def __repr__(self):
        return f'Brick {self.name} : ({self.ends})'


class Tower:
    def __init__(self):
        self.filled = {}
        self.bricks = {}
        self.order = []
        
    def add_brick(self, brick:Brick):
        self.bricks[brick.get_name()] = brick
        self.order.append(brick)
        for z, x, y in brick.get_positions():
            self.filled[(z, x, y)] = brick.get_name() 

    def sort_order(self):
        self.order.sort()

    def lower_brick(self, i):
        # i-th order
        # find able to move down
        b = self.order[i]
        # print("Lowering brick", i, b)
        diff = 0
        cont = True
        ontopof = set()
        while cont:
            for z, x, y in b.get_positions():
                if (z-diff-1) == 0:
                    cont = False
                    break
                elif (z-diff-1, x, y) in self.filled:
                    if self.filled[(z-diff-1, x, y)] != b.name:
                        ontopof.add(self.filled[(z-diff-1, x, y)])
                        cont = False
            
            if cont: diff += 1
            
        b.ontopof = ontopof

        # shift down
        for i, p in enumerate(b.positions):
            z, x, y = p
            # update
            del self.filled[(z, x, y)]
            self.filled[(z-diff, x, y)] = b.name
            b.positions[i] = (z-diff, x, y)
    
    def lower_all(self):
        for i, b in enumerate(self.order):
            self.lower_brick(i)
            
        
        
        
        
        
    

def parse_lines():
    lines = read_input_file(22)
    tower = Tower()
    for i, l in enumerate(lines):
        coords = l.replace('~', ',').split(',')
        b = Brick(i, *[int(x) for x in coords])
        tower.add_brick(b)

    return tower


def build_graph(tower):
    # A -> B : a supports b == b ontop of a
    supports = defaultdict(set)
    supportedby = defaultdict(set)
    
    for n, b in tower.bricks.items():
        for a in b.ontopof:
            supports[a].add(n)
            supportedby[n].add(a)
    
    return supports, supportedby
    


def fall_count(supportedby, n):
    # see how many other bricks would fall if brick n was removed
    graph = supportedby.copy()
    if n in graph: del graph[n]
    removed = set([n])
    cont = True
    while cont:
        cont = False
        for b, deps in graph.items():
            if len(deps - removed) == 0:
                cont = True
                removed.add(b)
        
        for r in removed:
            if r in graph: del graph[r]

    return len(removed)



def solution1():
    tower = parse_lines()
    tower.sort_order()
    tower.lower_all()

    supports, supportedby = build_graph(tower)
    count = 0
    for name, b in tower.bricks.items():
        if fall_count(supportedby, name) == 1:
            count += 1
    return count



def solution2():
    tower = parse_lines()
    tower.sort_order()
    tower.lower_all()

    supports, supportedby = build_graph(tower)
    count = 0
    for name, b in tower.bricks.items():
        count += fall_count(supportedby, name) - 1
    return count

    
    
    
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())