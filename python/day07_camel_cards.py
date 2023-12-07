# Day 7: Camel Cards
# https://adventofcode.com/2023/day/7

from typing import List
from util.input_util import read_input_file
from collections import deque, defaultdict, Counter
from enum import IntEnum 

class HandType(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_KIND = 4
    FULL_HOUSE = 5
    FOUR_KIND = 6
    FIVE_KIND = 7


def map_suit_to_num(suit:str) -> int:
    mapping = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, 'J': 1}
    return mapping[suit] if suit in mapping else int(suit)

def parse_cards(hand:str) -> List[int]:
    return [map_suit_to_num(h) for h in hand] 

class Hand:
    def __init__(self, cards:str, bid:int):
        self.bid = bid
        self.cards_raw = cards
        self.cards = parse_cards(cards) # maintain order
        self.counts = Counter(self.cards) # card -> count
        self.__aggregate_cards()
        self.hand_type = None


    def __aggregate_cards(self) -> None:
        self.cc = defaultdict(list) # count -> card list
        # count of pairs, threes, fours, etc
        for card, count in self.counts.items():
            self.cc[count].append(card)
            self.cc[count].sort(reverse=True) # sort in order high -> low

    def __hand_type(self) -> HandType:
        # check type
        if len(self.cc[5]) == 1: return HandType.FIVE_KIND
        if len(self.cc[4]) == 1: return HandType.FOUR_KIND
        if len(self.cc[3]) == 1 and len(self.cc[2]) == 1: return HandType.FULL_HOUSE
        if len(self.cc[3]) == 1: return HandType.THREE_KIND
        if len(self.cc[2]) == 2: return HandType.TWO_PAIR
        if len(self.cc[2]) == 1: return HandType.ONE_PAIR
        if len(self.cc[1]) == 5: return HandType.HIGH_CARD
        raise ValueError(f"Unknown hand type {self.cards}")


    def __hand_type_with_jokers(self) -> HandType:
        # If no joker
        maxtype = self.__hand_type()
        if 1 not in self.counts: maxtype

        n = self.counts[1] # number of jokers
        self.counts[1] = 0
        # try to change to other type and recalculate hand
        for c in self.counts:
            if c != 1: # if not joker, modify counts
                self.counts[c] += n
                self.__aggregate_cards()
                newtype = self.__hand_type()
                if newtype > maxtype:
                    maxtype = newtype
                self.counts[c] -= n
                
        # reset
        self.counts[1] = n
        self.__aggregate_cards()
        return maxtype 

    def set_hand_type(self) -> None:
        self.hand_type = self.__hand_type()
    
    def set_hand_type_with_jokers(self) -> None:
        self.hand_type = self.__hand_type_with_jokers()
    
    def __lt__(self, other:HandType) -> bool:
        if self.hand_type == other.hand_type:
            return self.cards < other.cards
        return self.hand_type < other.hand_type
    
    def __eq__(self, other:HandType) -> bool:
        if self.hand_type != other.hand_type: return False
        return self.cards == other.cards

    def __repr__(self) -> str:
        return f'Hand: {self.cards_raw} - {self.hand_type.name} - [{self.bid}]'

        

def parse_lines() -> List[Hand]:
    lines = read_input_file(7)
    hands = []
    for l in lines:
        h, b = l.split()
        hands.append(Hand(h, int(b)))
    return hands


def solution1():
    hands = parse_lines()
    for h in hands:
        h.set_hand_type()
    hands.sort()

    res = 0
    for i, h in enumerate(hands):
        # print(h)
        res += (i+1) * h.bid
    return res
    

    
def solution2():
    hands = parse_lines()
    for h in hands:
        h.set_hand_type_with_jokers()
    hands.sort()

    res = 0
    for i, h in enumerate(hands):
        # print(h)
        res += (i+1) * h.bid
    return res 
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())