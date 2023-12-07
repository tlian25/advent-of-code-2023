# Day 6: Wait For It
# https://adventofcode.com/2023/day/6

import math
from util.input_util import read_input_file

def parse_lines():
    lines = read_input_file(6)
    times = [int(x) for x in lines[0].split()[1:]]
    distances = [int(x) for x in lines[1].split()[1:]]
    return times, distances


# Times allowed for each race
# Best distance ever recorded in that race
# go further than current record holder

# Hold button charges boat, release allows the boat to move
# start speed of 0 mpms
# For each ms you spend holding down, boat speed increases by 1 mpms

# Determine the number of ways you can beat the record in each race
# multiple these values together


def calc_dist(h, t):
    # h = time to hold
    # t = total time
    return (t-h) * h

def number_of_ways_to_win(t, d):
    # number of ms to hold
    count = 0
    for i in range(1, t):
        if calc_dist(i, t) > d:
            count += 1
    return count
            


def solution1():
    times, distances = parse_lines()
    # print(times)
    # print(distances) 

    res = 1
    for i, t in enumerate(times):
        d = distances[i]
        ways2win = number_of_ways_to_win(t, d)
        # print(ways2win)
        res *= ways2win

    return res




def binary_search_upper(t, dist):
    # Need to find highest number that allows us to win
    # monotonically decreasing
    i, j = t//2, t
    while i < j:
        # print('\r', i, j, end='')
        m = (i+j) // 2
        d = calc_dist(m, t)
        if d == dist:
            return m
        elif d > dist:
            i = m+1
        else:
            j = m-1
    return i
             



def binary_search_lower(t, dist):
    # find lowest number that allows us to win
    # monotonically increasing
    i, j = 0, t//2
    while i < j:
        # print('\r', i, j, end='')
        m = (i+j) // 2
        d = calc_dist(m, t)
        if d == dist:
            return m
        elif d > dist:
            j = m-1
        else:
            i = m+1
    return j
    

    
def number_of_ways_to_win2(t, d):
    # Since we can't search all ways, we know it's a parabola.
    # We just need to solve for the two intersections
    # 0 = -x^2 + t*x - d

    # Use binary search
    upper = binary_search_upper(t, d)
    lower = binary_search_lower(t, d)

    # sanity check that one beyond upper is less and one below lower is less
    assert calc_dist(upper+1, t) < d
    assert calc_dist(lower-1, t) < d
    return upper - lower + 1
    

    
    
    
def solution2():
    times, distances = parse_lines()
    time = ''.join([str(x) for x in times])
    dist = ''.join([str(x) for x in distances])
    
    time = int(time)
    dist = int(dist)
    
    return number_of_ways_to_win2(time, dist)
    
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())