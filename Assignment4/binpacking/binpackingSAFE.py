#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Gaël Aglin <gael.aglin@uclouvain.be>"""
from search import *
import sys


class BinPacking(Problem):

    def successor(self, state):
        # First the successors using the move method
        for i, binA in enumerate(state.bins):
            for j, binB in enumerate(state.bins):
                if i != j:
                    for item, weight in binA.items():
                        #print(binB)
                        #print("passage", sum(list(binB.values())), state.capacity, weight)

                        if state.can_fit(binB, int(weight)):
                            #print('---------------')
                            #print(item, j, binB, weight)
                            #print('ici')
                            #print(item, binB)
                            newstate = state.copy_state()
                            newstate.bins[i].pop(item)
                            newstate.bins[j][item] = weight
                            #print(newstate.bins[i], newstate.bins[j])
                            if len(newstate.bins[i]) == 0:
                                del newstate.bins[i]
                            #print(len(newstate.bins))
                            yield (item, j), newstate
        # Second method using swap
        for i, binA in enumerate(state.bins):
            for j, binB in enumerate(state.bins):
                if i < j:
                    for itemA, weightA in binA.items():
                        for itemB, weightB in binB.items():
                            if weightA != weightB:
                                new_state = state.copy_state()
                                new_state.bins[i].pop(itemA)
                                new_state.bins[j].pop(itemB)
                                if new_state.can_fit(new_state.bins[i], int(weightB)) and new_state.can_fit(new_state.bins[j], int(weightA)):
                                    new_state.bins[i][itemB] = weightB
                                    new_state.bins[j][itemA] = weightA
                                    #print('test debut', new_state.bins[i].keys(), itemA)
                                    #print("swap", new_state.bins)
                                    yield None, new_state

    def fitness(self, state):
        """
        :param state:
        :return: fitness value of the state in parameter
        """
        fitness = 0
        k = len(state.bins)
        for bin in state.bins:
            fullness = 0
            for weight in bin.values():
                fullness += int(weight)
            fitness += (fullness / state.capacity) ** 2
            #print("kkk", fullness/state.capacity, state.capacity)
        #print(1 - fitness / k)
        return 1 - fitness / k


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
        possible_moves = list(best.expand())
        if possible_moves is None or len(possible_moves) == 0:
            return best
        best_next = None
        best_value = math.inf
        for next in possible_moves:
            value = problem.fitness(next.state)
            if value < best_value:
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
        possible_moves = list(best.expand())
        five_best = [(math.inf, None)] * 5
        if possible_moves is None or len(possible_moves) == 0:
            #print("ONLY ONE")
            return best
        for next in possible_moves:
            value = problem.fitness(next.state)
            if value < five_best[0][0]:
                five_best[0] = (value, next)
                five_best.sort(key=lambda x: x[0], reverse=True)
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
    step_limit = 100
    #node = randomized_maxvalue(bp_problem, step_limit)
    node = maxvalue(bp_problem, step_limit)
    state = node.state
    #print(bp_problem.fitness(state))
    print(state)
    #print(init_state)
    #sum = 0
    #print(maxvalue(bp_problem).state)
    #print(randomized_maxvalue(bp_problem).state)
