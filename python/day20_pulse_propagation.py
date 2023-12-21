# Day 20: Pulse Propagation
# https://adventofcode.com/2023/day/20

from util.input_util import read_input_file
from collections import deque, defaultdict
import math

# Flipflop %: on or off, initially off, ignore HIGH, flip on LOW
#   if flip off -> send LOW, if flip on -> send HIGH
# Conjuction &: remember last pulse, initial LOW, 
# Broadcast: single module - sends same pulse to all dest
# Button: when push -> send LOW to broadcast

FLIPFLOP = '%'
CONJUNCTION = '&'
BROADCASTER = 'broadcaster'
RX = 'rx'
BUTTON = 'button'
OUTPUT = 'output'

HIGH = 'high'
LOW = 'low'
OFF = 'off'
ON = 'on'

class ModuleManager:
    def __init__(self, modules:dict):
        self.modules = modules
        self.q = deque()
        self.counts = {LOW: 0, HIGH:0}
        self.cycles = {}
        self.found = 0
        for nm, m in self.modules.items():
            m.attach_queue(self.q)

    def run(self, i=0):
        # Sender, Receiver, Signal 
        self.q.append((BUTTON, BROADCASTER, LOW))
        while self.q:
            sender, receiver, signal = self.q.popleft()
            self.counts[signal] += 1
            m = self.modules[receiver]
            m.receive(signal, sender)
            if signal == HIGH and sender in self.cycles and self.cycles[sender] is None:
                self.found += 1
                self.cycles[sender] = i

    
    def get_counts(self):
        return self.counts[HIGH], self.counts[LOW]
        


class Module:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.state = OFF
        self.last = {}
        self.dest = []
        self.counts = {LOW: 0, HIGH:0}
        self.outputs = []
        
    def attach_queue(self, q):
        self.q = q

    def add_dest(self, dest):
        self.dest.append(dest)
        dest.last[self.name] = LOW # callback for CONJUNCT
    
    def receive(self, signal, sendername):
        self.counts[signal] += 1
        if self.type in (BUTTON, BROADCASTER):
            self.send(signal)
        elif self.type == OUTPUT:
            self.outputs.append(signal)
        elif self.type == FLIPFLOP:
            if signal == LOW:
                if self.state == OFF:
                    self.state = ON
                    self.send(HIGH)
                else:
                    self.state = OFF
                    self.send(LOW)
        elif self.type == CONJUNCTION:
            self.last[sendername] = signal
            if all([x == HIGH for x in self.last.values()]):
                self.send(LOW)
            else:
                self.send(HIGH)

    def send(self, signal):
        for d in self.dest:
            # print(f"{self.name} --{signal}--> {d.name}")
            self.q.append((self.name, d.name, signal))
            
            
    def get_counts(self):
        return self.counts[HIGH], self.counts[LOW]
    
    def get_cycle(self):
        return self.state_change_cycle
    
    def __repr__(self):
        s = f'[{self.name}] ({self.type}) - {[x.name for x in self.dest]}'
        return s


def parse_lines():
    lines = read_input_file(20)
    # scan through once and create all modules 
    modules = {BUTTON: Module(BUTTON, BUTTON),
               OUTPUT: Module(OUTPUT, OUTPUT),
               BROADCASTER: Module(BROADCASTER, BROADCASTER),
               RX: Module(RX, RX)}

    for l in lines:
        src, dests = l.split(' -> ')
        if src != BROADCASTER:
            type = src[0]
            name = src[1:]
            if name not in modules:
                modules[name] = Module(name, type)

    # scan through again to make connections
    for l in lines:
        src, dests = l.split(' -> ')
        if src == BROADCASTER:
            name = BROADCASTER
        else:
            name = src[1:]

        for d in dests.split(', '):
            modules[name].add_dest(modules[d])
    
    modules[BUTTON].add_dest(modules[BROADCASTER])
    return modules
        

def solution1():
    modules = parse_lines()
    modman = ModuleManager(modules)

    for i in range(1000):
        modman.run()
        
    h, l = modman.get_counts()
    return h * l
        

def solution2():
    modules = parse_lines()
    modman = ModuleManager(modules)
    rx = modules[RX]

    # dg sends to rx
    # All modules that send to dg
    for n, m in modules.items():
        for d in m.dest:
            if d.name == 'dg':
                modman.cycles[n] = None

    # need to find cycle for all these to flip to HIGH
    i = 0
    while modman.found < len(modman.cycles):
        i += 1
        modman.run(i)

    return math.lcm(*modman.cycles.values())

    
    
if __name__ == '__main__':
    print("Part 1:", solution1())
    
    print('--------------')
    
    print("Part 2: ", solution2())