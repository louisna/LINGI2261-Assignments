#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Gaël Aglin <gael.aglin@uclouvain.be>"""
from search import *
import sys


class BinPacking(Problem):

    def successor(self, state):
        """
        Gives all the successors of state
        The successors are given by the move and the swap methods (defined in the statement)
        :param state: the state to be expanded
        :return: yields all the successors. First using move, then using swap
        """
        # First the successors using the move method
        # For each bin, we take each object currently in the bin (one at a time)
        # and move it to another bin if possible (if it fits)
        for i, binA in enumerate(state.bins):
            for j, binB in enumerate(state.bins):
                # Disable stupid moves
                if i != j:
                    for item, weight in binA.items():
                        # If item fits in binB
                        if state.can_fit(binB, int(weight)):
                            # Duplicate the current state
                            newstate = state.copy_state()
                            # Pop item from bin i of the copied state...
                            newstate.bins[i].pop(item)
                            # ..And put it in bin j of the copied state
                            newstate.bins[j][item] = weight
                            # Remove the bin from the copied state if there aren't any object in it
                            # i.e. we moved the last item from this bin
                            if len(newstate.bins[i]) == 0:
                                del newstate.bins[i]
                            yield (item, j), newstate

        # Second method using swap
        # For each bin, we swap each items (one at a time) which an object from another bin
        for i, binA in enumerate(state.bins):
            for j, binB in enumerate(state.bins):
                # To avoid duplicated state, i.e. make a swap from bin 1 to bin 3 is exactly the same as
                # making a swap from bin 3 to bin 1
                if i < j:
                    for itemA, weightA in binA.items():
                        for itemB, weightB in binB.items():
                            # If the weights are the same, then the swap is useless: we get no improvement
                            if weightA != weightB:
                                # Copy of the state
                                new_state = state.copy_state()
                                # Pop the two items before swapping
                                new_state.bins[i].pop(itemA)
                                new_state.bins[j].pop(itemB)
                                # See if we put the two items in the new bins, it fits
                                if new_state.can_fit(new_state.bins[i], int(weightB)) and new_state.can_fit(
                                        new_state.bins[j], int(weightA)):
                                    # Add items to their new bons
                                    new_state.bins[i][itemB] = weightB
                                    new_state.bins[j][itemA] = weightA
                                    yield (i, j, itemA, itemB), new_state

    def fitness(self, state):
        """
        Gives the fitness value of the state, according to the statement definition
        :param state: the state used to compute the fitness
        :return: fitness value of the state in parameter
        """
        fitness = 0
        k = len(state.bins)
        for bin in state.bins:
            fullness = 0
            for weight in bin.values():
                fullness += int(weight)
            fitness += (fullness / state.capacity) ** 2
        return 1 - fitness / k

    def value(self, state):
        return self.fitness(state)


class State:

    def __init__(self, capacity, items, generate=True, which=1):
        """
        Creates an object of class State. It is a bit modified from the initial method, to handle specific purposes
        :param capacity: the capacity of the bins
        :param items: the items
        :param generate: True if the creation of the object will build a basic solution
                        This argument allows the computation of the successor function more quickly:
                        We know that we won't use the initial bins value computed by build_init(2), because
                        if generate=False, we know we are currently making a copy of a state
        :param which: 1 calls build_init, 2 calls build_init2. Used to perform 2 different kinds of initialisations
                        to get two different solutions and compare them
        """
        self.capacity = capacity
        self.items = items
        if generate:
            if which == 1:
                self.bins = self.build_init()
            else:
                self.bins = self.build_init2()

    def copy_state(self):
        """
        Makes a copy of the state 'self'. A copy is done by creating a new State, and gives a copy of the layout of the
        bins
        :return: a copy of the state 'self'
        """
        new_state = State(self.capacity, self.items.copy(), generate=False)
        new_state.bins = [bin.copy() for bin in self.bins]
        return new_state

    # an init state building is provided here but you can change it at will
    def build_init(self):
        """
        Initial build, given in the statement. Tries to full the last created bin. If not possible, creates a new bin
        and put the current object in it
        :return: the bins' layout
        """
        init = []
        for ind, size in self.items.items():
            if len(init) == 0 or not self.can_fit(init[-1], size):
                init.append({ind: size})
            else:
                if self.can_fit(init[-1], size):
                    init[-1][ind] = size
        return init

    def build_init2(self):
        """
        Second method of initialisation for the bins. This function gives a new bin for each item.
        Even if it is a very bad initialisation, it can give good results.
        :return: the bins' layout
        """
        init = []
        for ind, size in self.items.items():
            init.append({ind: size})
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
    """
    Function defined in the statement.
    """
    current = LSNode(problem, problem.initial, 0)
    best = current

    for step in range(limit):
        # This condition is just the same as in the random walk
        if callback is not None:
            callback(current)
        # Get all possible moves
        possible_moves = list(best.expand())
        # If there are no possible moves, we return the best so far. Should not happen in non-trivial instances
        if possible_moves is None or len(possible_moves) == 0:
            return best
        # best_next is the state of the best next move to do
        best_next = None
        best_value = math.inf
        for next in possible_moves:
            # Compute the fitness
            value = problem.fitness(next.state)
            # If the value of the state 'next' is better than the best next's value...
            if value < best_value:
                # ... we update the best next
                best_next = next
                best_value = value
        # Best is updated at each iteration, even if it degrades the optimal value
        best = best_next
    return best


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100, callback=None):
    """
        Function defined in the statement.
    """
    current = LSNode(problem, problem.initial, 0)
    best = current

    for step in range(limit):
        # This condition is just the same as in the random walk
        if callback is not None:
            callback(current)
        # Get all possible moves
        possible_moves = list(best.expand())
        five_best = [(math.inf, None)] * 5
        # If there are no possible moves, we return the best so far. Should not happen in non-trivial instances
        if possible_moves is None or len(possible_moves) == 0:
            return best
        for next in possible_moves:
            # Compute the fitness
            value = problem.fitness(next.state)
            # If the value is better than the "worst" value of the best successors
            if value < five_best[0][0]:
                # We replace it...
                five_best[0] = (value, next)
                # ... And sort the list after
                five_best.sort(key=lambda x: x[0], reverse=True)
        # Best is updated at each iteration, even if it degrades the optimal value
        # Best is updated with one of the 5 best moves discovered for the iteration
        best = random.choice(five_best)[1]
    return best


#####################
#       Launch      #
#####################

if __name__ == '__main__':
    info = read_instance(sys.argv[1])
    # First, we make the computation with build_init
    init_state = State(info[0], info[1], which=1)
    bp_problem = BinPacking(init_state)
    bp_problem.successor(init_state)
    step_limit = 300
    node = random_walk(bp_problem, step_limit)
    state = node.state
    # Then, we make the computation with build_init2
    # init_state2 = State(info[0], info[1], which=2)
    # bp_problem2 = BinPacking(init_state2)
    # bp_problem2.successor(init_state2)
    # node2 = maxvalue(bp_problem2, step_limit)
    # state2 = node2.state
    # Compare the two results, and print out the state giving the best fitness
    # if bp_problem.fitness(state) < bp_problem2.fitness(state2):
    #    print(state)
    # else:
    #    print(state2)
    print(state)
