# Day 5: If You Give a Seed a Fertilizer
# https://adventofcode.com/2023/day/5

from util.input_util import read_input_file


class Mapping:
    def __init__(self, src:str, dst:str):
        self.src = src
        self.dst = dst
        self.src_ranges = [] # list of tuples
        self.dst_ranges = {} # (src_start, src_end) -> dst_start
        self.cache = {}
        
    def get_src(self) -> str:
        return self.src
    
    def get_dst(self) -> str:
        return self.dst

    def add_range(self, src_start:int, dst_start:int, length:int) -> None:
        # start, end - inclusive
        src_end = src_start+length-1
        self.src_ranges.append((src_start, src_end))
        self.src_ranges.sort()
        self.dst_ranges[(src_start, src_end)] = dst_start
    
    def get_mapping(self, src:int) -> int:
        if src in self.cache: return self.cache[src]

        start, end = self.binary_search(src)
        if start <= src <= end:
            diff = src - start
            self.cache[src] = self.dst_ranges[(start, end)] + diff
            return self.cache[src]
            
        self.cache[src] = src
        return src

        
    def binary_search(self, src:int) -> tuple:
        # find first tuple with start <= src
        # then check if in tuple
        i, j = 0, len(self.src_ranges)
        while i<j:
            m = (i+j) // 2
            # print(m, src, self.src_ranges[m])
            if self.src_ranges[m][0] > src:
                j = m
            else:
                i = m+1

        start, end = self.src_ranges[j-1]
        if start <= src <= end:
            return (start, end) 
        return (-1, -1)
    
    def __repr__(self):
        s = f"[{self.src} -> {self.dst}]\n{self.dst_ranges}"
        return s
        
        

def parse_lines():
    lines = read_input_file(5)
    seeds = [int(x) for x in lines[0].replace("seeds: ", "").split()]
    mappings = {}
    currMap = None

    for l in lines[2:]:
        if l == "":
            continue
        elif "map" in l:
            # seed-to-soil map:
            src, _, dst = l.split()[0].split('-')
            currMap = Mapping(src, dst)
            mappings[src] = currMap
        else:
            dst_start, src_start, length = l.split()
            currMap.add_range(int(src_start), int(dst_start), int(length))
            
    return seeds, mappings


# dest range start, src range start, range length
# any src numbers that aren't mapped correspond to the same dest
# 

def trace_mappings(seed:int, mappings:dict) -> int:
    src = 'seed'
    curr = seed
    while src != 'location':
        print(curr)
        m = mappings[src]
        curr = mappings[src].get_mapping(curr)
        src = m.get_dst()
    
    return curr



def solution1():
    seeds, mappings = parse_lines()
    minloc = float('inf')

    for s in seeds:
        print("Seed", s)
        loc = trace_mappings(s, mappings)
        minloc = min(minloc, loc)
    
    return minloc



    
def solution2():
    seed_ranges_raw, mappings = parse_lines()
    minloc = float('inf')

    
    # Try to get all boundary values from all mappings
    # We know min has to be on the boundary somewhere
    boundaries = [] # all distinct values to consider
    seed_ranges = [] # tuples of (start, end)
    for i in range(0, len(seed_ranges_raw), 2):
        start = seed_ranges_raw[i]
        l = seed_ranges_raw[i+1]
        end = start+l
        seed_ranges.append((start, end))
        boundaries += [start, end]
    
    # Include distinct values from the various mappings
    for _, m in mappings.items():
        for (a, b), c in m.dst_ranges.items():
            boundaries += [a, b, c]

    for s in boundaries:
        # Only consider boundary unit if within original seed ranges
        for r0, r1 in seed_ranges:
            if r0 <= s <= r1:
                loc = trace_mappings(s, mappings)
                minloc = min(minloc, loc)
    
    return minloc



if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    # print("Part 2: ", solution2())