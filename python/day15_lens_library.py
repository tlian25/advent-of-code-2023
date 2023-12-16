# Day 15: Lens Library
# https://adventofcode.com/2023/day/15

from util.input_util import read_input_file
from collections import deque, defaultdict

def parse_lines():
    lines = read_input_file(15)
    inputs = lines[0].split(',')
    return inputs


# HASH: string -> int
# Curr val = 0
# Determine ASCII code
# Increase value by ASCII code
# multiply by 17
# mod 256

def hash(s:str) -> int:
    val = 0
    for letter in s:
        val += ord(letter)
        val *= 17
        val %= 256
    return val

# = : followed by a number indicating focal length of the lens that needs to go into box
# - : go to relevant box and remove the lens with the given label if present
    
class HashMap:
    def __init__(self):
        self.map = [[] for _ in range(256)] # keeps ordering
        self.contains = [set() for _ in range(256)] # fast check inclusion

    def operate(self, s):
        if '=' in s:
            s, i = s.split('=')
            self.add(s, int(i))
        else:
            self.remove(s[:-1])

    def add(self, s, focal):
        n = hash(s)
        if s in self.contains[n]:
            # replace
            idx = self.find_index(s, n)
            self.map[n][idx][1] = focal
        else:
            self.contains[n].add(s)
            self.map[n].append([s, focal])

    def remove(self, s):
        n = hash(s)
        if s in self.contains[n]:
            idx = self.find_index(s, n)
            self.map[n] = self.map[n][:idx] + self.map[n][idx+1:]
            self.contains[n].remove(s)
        # else do nothing
            
    def find_index(self, s, n):
        for i in range(len(self.map[n])):
            if self.map[n][i][0] == s:
                return i
        
    def focus_power(self):
        total = 0
        for n in range(256):
            for i, s in enumerate(self.map[n]):
                focus = (n+1) * (i+1) * s[1]
                total += focus
        return total



def solution1():
    inputs = parse_lines()

    totalhash = 0
    for s in inputs:
        val = hash(s)
        # print(s, val)
        totalhash += val
    return totalhash
    
    
def solution2():
    inputs = parse_lines()
    hm = HashMap() 

    for s in inputs:
        hm.operate(s)
    
    return hm.focus_power()
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())