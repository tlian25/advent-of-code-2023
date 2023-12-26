# Day 24: Never Tell Me The Odds
# https://adventofcode.com/2023/day/24

from util.input_util import read_input_file
from collections import deque, defaultdict
from itertools import combinations
import numpy as np
import z3



# Test Section
X0, X1 = 200000000000000, 400000000000000 
Y0, Y1 = 200000000000000, 400000000000000 

class Hailstone:
    def __init__(self, i, l):
        self.name = i
        pos, vel = l.split(' @ ')
        self.pos = [int(x) for x in pos.split(', ')]
        self.vel = [int(x) for x in vel.split(', ')]
    
    def will_intersect_xy(self, other):
        # x = a * t + b
        # y = c * t + d
        a1, b1, c1, d1 = self.vel[0], self.pos[0], self.vel[1], self.pos[1]
        slope1 = c1 / a1
        inter1 = d1 - b1 * c1 / a1

        a2, b2, c2, d2 = other.vel[0], other.pos[0], other.vel[1], other.pos[1]
        slope2 = c2 / a2
        inter2 = d2 - b2 * c2 / a2

        if slope1 == slope2: return False
        
        # y = m1 * x + b1
        # y = m2 * x + b2
        x = (inter2 - inter1) / (slope1 - slope2)
        y = slope1 * x + inter1

        # check within boundaries
        if x < X0 or x > X1 or y < Y0 or y > Y1: return False
    
        # check negative time
        t1 = (x - b1) / a1
        t2 = (x - b2) / a2
        if t1 < 0 or t2 < 0: return False
        return True
        

    
    def __repr__(self):
        return f'[Hailstone {self.name}] - {self.pos} @ {self.vel}'


def parse_lines():
    lines = read_input_file(24)
    hailstones = []
    for i, l in enumerate(lines):
        hailstones.append(Hailstone(i, l))
    return hailstones




def solution1():
    hailstones = parse_lines()
    count = 0
    for h1, h2 in combinations(hailstones, 2):
        # print(h1)
        # print(h2)
        i = h1.will_intersect_xy(h2)
        # print(i)
        if i: count += 1
    return count


def solution2():
    # magic from reddit...
    """
    Solve for 9 variables:

    three points in times: t,u,v
    stone starting location: a,b,c
    stone starting speed: d,e,f

    stone:  S(t) = (a,b,c) + (d,e,f)*t
    hail 0: H0(t) = A0 + t*V0
    hail 1: H1(t) = A1 + t*V1
    hail 2: H2(t) = A2 + t*V2

    The stone trajectory intersects the three hails at three different times:
    S(t) = H0(t)
    S(u) = H1(u)
    S(v) = H2(v)

    Each of these gives rise to three equations (in the x, y, and z axes),
    giving the total of nine below.
    """
    puzzle = np.fromregex('../inputs/day24_input.txt', r"-?\d+", [('', int)]).astype(int).reshape(-1, 2, 3)
    three = puzzle[:3]
    t, u, v, a, b, c, d, e, f = z3.Reals("t u v a b c d e f")
    (A0x, A0y, A0z), (V0x, V0y, V0z) = three[0]
    (A1x, A1y, A1z), (V1x, V1y, V1z) = three[1]
    (A2x, A2y, A2z), (V2x, V2y, V2z) = three[2]
    eqs = [
        a + t * d == A0x + t * V0x,
        b + t * e == A0y + t * V0y,
        c + t * f == A0z + t * V0z,
        a + u * d == A1x + u * V1x,
        b + u * e == A1y + u * V1y,
        c + u * f == A1z + u * V1z,
        a + v * d == A2x + v * V2x,
        b + v * e == A2y + v * V2y,
        c + v * f == A2z + v * V2z,
    ]
    s = z3.Solver()
    s.add(*eqs)
    s.check()
    r = s.model()
    pos = [r[x].as_long() for x in [a, b, c]]
    print(pos)
    return sum(pos)
    
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())