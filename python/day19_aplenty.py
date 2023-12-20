# Day 19: Aplenty
# https://adventofcode.com/2023/day/19

from util.input_util import read_input_file
from collections import deque, defaultdict

X = 'x'
M = 'm'
A = 'a'
S = 's'

REJECTED = 'R'
ACCEPTED = 'A'

class Workflow:
    def __init__(self, name:str):
        self.name = name
        self.rules = [] # list of lambda functions
        self.rules2 = [] # list of ranges (letter, dest, start, end)
        self.cutoffs = defaultdict(list)
    
    # Initial Attempt. Works for Part 1. Converts each rule to a lambda function.
    def add_rule(self, rule):
        # parse rule
        if ':' in rule:
            r, dest = rule.split(':')
            if '<' in r:
                p, amt = r.split('<')
                l = lambda x : x[p] < int(amt)
            elif '>' in r:
                p, amt = r.split('>')
                l = lambda x : x[p] > int(amt)
            self.cutoffs[p].append(int(amt))
        else:
            l = lambda x : True
            dest = rule
        self.rules.append((l, dest))
        
    def process(self, part):
        for rule, dest in self.rules:
            if rule(part): return dest
    
    # For Part 2. Uses range of values to compare against instead of lambda function.
    def add_rule2(self, rule):
        if ':' in rule:
            r, dest = rule.split(':')
            if '<' in r:
                p, amt = r.split('<')
                self.rules2.append((p, dest, 1, int(amt)-1))
            elif '>' in r:
                p, amt = r.split('>')
                self.rules2.append((p, dest, int(amt)+1, 4000))
        else:
            # No conditional, only destination. So apply dummy rule for accepting all possible values of X
            self.rules2.append((X, rule, 1, 4000))

    def process2(self, part):
        for p, dest, start, end in self.rules2:
            if start <= part[p] <= end: return dest


def parse_lines():
    lines = read_input_file(19)
    workflows = {}

    for i, l in enumerate(lines):
        if l == "": break
        nm, rules = l.split('{')
        w = Workflow(nm)
        for rule in rules.replace('}','').split(','):
            w.add_rule(rule)
            w.add_rule2(rule)
        workflows[nm] = w

    parts = []
    for l in lines[i+1:]:
        part = {}
        for p in l[1:-1].split(','):
            k, v = p.split('=')
            part[k] = int(v)
        parts.append(part)
    return workflows, parts


def process_all_workflows(part, workflows):
    wfname = 'in'
    while wfname not in (ACCEPTED, REJECTED):
        wf = workflows[wfname]
        wfname = wf.process2(part)
    return wfname


def solution1():
    workflows, parts = parse_lines()
    res = 0
    for part in parts:
        approval = process_all_workflows(part, workflows)
        if approval == ACCEPTED:
            res += sum(part.values())
    return res
        

    
    
def solution2():
    # take all possible values for each value xmas
    # each one is 1-4000
    workflows, parts = parse_lines()

    # BFS all possible range combinations
    q = deque([('in', {X:(1, 4000), M:(1, 4000), A:(1,4000), S:(1,4000)})])
    acceptedranges = []
    while q:
        curr, part = q.popleft()
        if curr == ACCEPTED:
            acceptedranges.append(part)
            continue
        elif curr == REJECTED:
            continue

        curr = workflows[curr]
        for i in range(len(curr.rules2)):
            # Apply current rule
            copypart = part.copy()
            p, dest, start, end = curr.rules2[i]
            copypart[p] = (max(copypart[p][0], start), min(copypart[p][1], end))

            # Negate all previous rules - otherwise would not have reached current rule
            for j in range(i):
                p, _, start, end = curr.rules2[j]
                if start == 1: # <
                    start, end = end+1, 4000
                elif end == 4000: # >
                    start, end = 1, start-1
                else:
                    raise ValueError("Unknown rule", p, start, end)
                copypart[p] = (max(copypart[p][0], start), min(copypart[p][1], end))

            q.append((dest, copypart))

    total = 0
    for part in acceptedranges:
        # Multiply all ranges for each ACCEPTED part range
        subtotal = 1
        for p, (start, end) in part.items():
            subtotal *= (end - start + 1) 
        total += subtotal
    return total



if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())