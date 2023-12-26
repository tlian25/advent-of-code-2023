# Day 25: Snowverload
# https://adventofcode.com/2023/day/25

from util.input_util import read_input_file
from collections import deque, defaultdict
from itertools import combinations
import math

def parse_lines():
    lines = read_input_file(25)
    graph = defaultdict(set)
    for l in lines:
        node, nbs = l.split(': ')
        nbs = nbs.split()
        for n in nbs:
            graph[node].add(n)
            graph[n].add(node)
    return graph

def bfs(node, graph):
    q = deque([node])
    seen = set([node])
    while q:
        curr = q.popleft()
        for nb in graph[curr]:
            if nb not in seen:
                seen.add(nb)
                q.append(nb)
    return seen

def connected_components(graph):
    connected = []
    total_seen = set()
    for node in graph:
        if node not in total_seen:
            seen = bfs(node, graph)
            connected.append(seen)
            total_seen = total_seen.union(seen)
    return connected

def extract_wires(graph):
    wires = set()
    for node in graph:
        for nb in graph[node]:
            if (node, nb) not in wires and (nb, node) not in wires:
                wires.add((node, nb))
    return wires


def group_by_nb_count(graph):
    nbs = defaultdict(set)
    for node in graph:
        nbcount = len(graph[node])
        nbs[nbcount].add(node)
    return nbs


def remove_wire(n1, n2, graph):
    graph[n1].remove(n2)
    graph[n2].remove(n1)


def add_wire(n1, n2, graph):
    graph[n1].add(n2)
    graph[n2].add(n1)


def shortest_path(n1, n2, graph):
    q = deque([(n1, 0)])
    seen = set([n1])
    while q:
        curr, steps = q.popleft()
        if curr == n2:
            return steps
        else:
            for nb in graph[curr]:
                if nb not in seen:
                    seen.add(nb)
                    q.append((nb, steps+1))
    return -1


def solution1():
    graph = parse_lines()
    wires = extract_wires(graph)

    paths = []
    for n1, n2 in wires:
        remove_wire(n1, n2, graph)
        p = shortest_path(n1, n2, graph)
        paths.append((p, n1, n2))
        add_wire(n1, n2, graph)
    
    paths.sort(reverse=True)

    # remove top 3 longest shortest paths
    for _, n1, n2 in paths[:3]:
        remove_wire(n1, n2, graph)

    cc = connected_components(graph)
    assert len(cc) == 2, len(cc)

    return len(cc[0]) * len(cc[1])
        




def solution2():
    pass
    
    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())