#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Gaël Aglin <gael.aglin@uclouvain.be>"""
from search import *
import sys


class BinPacking(Problem):

    def successor(self, state):
        # First the successors using the move method
        for i, binA in enumerate(state.bins):
            for j, binB in enumerate(state.bins):
                if binA != binB:
                    for item, weight in binA.items():
                        if state.can_fit(binB, int(weight)):
                            print(item, binB)
                            newstate = state.copy_state()
                            newstate.bins[i].pop(item)
                            newstate.bins[j][item] = weight
                            yield None, newstate

    def fitness(self, state):
        """
        :param state:
        :return: fitness value of the state in parameter
        """
        fitness = 0
        k = len(state.bins)
        for bin in state.bins:
            capacity_i = 0
            for _, weight in enumerate(bin):
                capacity_i += (int(weight) / state.capacity) ** 2
            fitness -= capacity_i / k
        return 1 + fitness


class State:

    def __init__(self, capacity, items):
        self.capacity = capacity
        self.items = items
        self.bins = self.build_init()
    
    def copy_state(self):
        new_state = State(self.capacity, self.items.copy())
        new_state.bins = [bin.copy() for bin in self.bins]
        return new_state

    # an init state building is provided here but you can change it at will
    def build_init(self):
        init = []
        for ind, size in self.items.items():
            if len(init) == 0 or not self.can_fit(init[-1], size):
                init.append({ind: size})
            else:
                if self.can_fit(init[-1], size):
                    init[-1][ind] = size
        return init

    def can_fit(self, bin, itemsize):
        return sum(list(bin.values())) + itemsize <= self.capacity

    def __str__(self):
        s = ''
        for i in range(len(self.bins)):
            s += ' '.join(list(self.bins[i].keys())) + '\n'
        return s


def read_instance(instanceFile):
    file = open(instanceFile)
    capacitiy = int(file.readline().split(' ')[-1])
    items = {}
    line = file.readline()
    while line:
        items[line.split(' ')[0]] = int(line.split(' ')[1])
        line = file.readline()
    return capacitiy, items

# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current

    for step in range(limit):
        if callback is not None:
            callback(current)
        # Choose the best node from successors
        possible_moves = list(current.expand())
        if possible_moves is None or len(possible_moves) == 0:
            print("ERROR !!!!!!!!")
            return
        best_next = possible_moves[0]
        best_value = problem.fitness(best_next.state)
        for next in possible_moves:
            value = problem.fitness(next.state)
            if value > best_value:
                best_next = next
                best_value = value
        best = best_next
    return best

# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current

    for step in range(limit):
        if callback is not None:
            callback(current)
        # Choose the best node from successors
        possible_moves = list(current.expand())
        five_best = [(-math.inf, None)] * 5
        if possible_moves is None or len(possible_moves) == 0:
            print("ERROR !!!!!!!!")
            return
        for next in possible_moves:
            value = problem.fitness(next.state)
            if value > five_best[0][0]:
                five_best[0] = (value, next)
                five_best.sort(key=lambda x: x[0])
        best = random.choice(five_best)[1]

    return best


#####################
#       Launch      #
#####################

if __name__ == '__main__':
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1])
    bp_problem = BinPacking(init_state)
    bp_problem.successor(init_state)
    step_limit = 300
    #node = randomized_maxvalue(bp_problem, step_limit)
    node = maxvalue(bp_problem, step_limit)
    state = node.state
    print(bp_problem.fitness(state))
    print(state)
    print(init_state)
    #print(maxvalue(bp_problem).state)
    #print(randomized_maxvalue(bp_problem).state)
