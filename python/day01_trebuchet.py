# Day 1: Trebuchet?1
# https://adventofcode.com/2023/day/1

from typing import Tuple, List
from util.input_util import read_input_file

def parse_lines() -> List[str]:
    lines = read_input_file(1)
    return lines

def is_digit(c:str):
    return '0' <= c <= '9'

def first_last_digit(line:str) -> Tuple[int, int]:
    first = None
    last = None
    for c in line:
        if is_digit(c):
            if not first:
                first = int(c)
            last = int(c)
    
    return first, last


def solution1():
    lines = parse_lines()

    s = 0
    for l in lines:
        first, last = first_last_digit(l)
        s += first * 10 + last
    return s
        

word2int = {'zero': 0,
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine':9}


def first_last_digit_words(line:str) -> Tuple[int, int]:
    first = None
    last = None
    for i, c in enumerate(line):
        if is_digit(c):
            if not first:
                first = int(c)
            last = int(c)

        for j in range(i+1, min(i+5, len(line))+1):
            ss = line[i:j]
            if ss in word2int:
                if not first:
                    first = word2int[ss]
                last = word2int[ss]

    return first, last
        

    
def solution2():
    lines = parse_lines()

    s = 0
    for l in lines:
        first, last = first_last_digit_words(l)
        s += first * 10 + last
    return s 
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())