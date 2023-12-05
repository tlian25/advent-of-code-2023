# Day 4: Scratchcards
# https://adventofcode.com/2023/day/4

from util.input_util import read_input_file
from collections import deque

class ScratchCard:
    def __init__(self, card:int, winNums:set, myNums:set):
        self.card = card
        self.winNums = winNums
        self.myNums = myNums
        self.wins = self.myNums.intersection(self.winNums)
    
    def score(self) -> int:
        n = len(self.wins)
        if n == 0: return 0
        return 2 ** (n-1)

    def getWins(self) -> set:
        return self.wins
    
    def getWinsCount(self) -> int:
        return len(self.wins)
    
    def getNum(self) -> int:
        return self.card
        
    def __repr__(self):
        return f"CARD: {self.card}\nWINNING: {self.winNums}\nMY: {self.myNums}\nWINS: {self.wins}"
        
        

def parse_lines():
    lines = read_input_file(4)
    cards = {}
    for l in lines:
        c, l = l[:l.find(':')], l[l.find(':')+2:]
        c = int(c.split()[1])
        win, my = l.split(' | ')
        win = set([int(x) for x in win.split()])
        my = set([int(x) for x in my.split()])
        card = ScratchCard(c, win, my)
        cards[c] = card
        
    return cards




def solution1():
    cards = parse_lines()
    totalscore = 0
    for _, card in cards.items():
        totalscore += card.score()
    
    return totalscore
        
    
    
def solution2():
    cards = parse_lines()
    counts = {c:1 for c in cards}
    totalcards = 0
    
    for c, card in cards.items():
        n = counts[c]
        totalcards += n

        for i in range(card.getWinsCount()):
            counts[c+i+1] += n
        
    return totalcards
        
    
    
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())