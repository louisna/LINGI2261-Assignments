# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gael Aglin <gael.aglin@uclouvain.be>'''
import time
import sys
from search import *


#################
# Problem class #
#################
class Knight(Problem):

    def successor(self, state):
        (x, y) = state.get_white()
        l = self.get_successor(x, y, state)
        l.sort(key=lambda t: -len(self.get_successor(t[0], t[1], state)))
        for (nx, ny) in l:
            yield ((nx, ny), self.new_state(nx, ny, state, x, y))

    def goal_test(self, state):
        for i in state.grid:
            if " " in i:
                return False
        return True

    def get_successor(self, x, y, state):
        p = ((1, -2), (-2, -1), (-1, 2), (-2, 1), (-1, -2), (1, 2), (2, 1), (2, -1))
        return [(x+i, y+j) for (i,j) in p if 0 <= x+i < state.nRows and 0 <= y+j < state.nCols and state.grid[x+i][y+j] == " "]

    def key_sort_successors(self, him, other, state):
        """
        A comparator using the number of successors of the node
        :param him: of the form (x, y) for the positions of him
        :param other: of the form (x, y) for the positions of him
        :return: 1, -1 or 0
        """
        return len(self.get_successor(him[0], him[1], state)) - len(self.get_successor(other[0], other[1], state))

    def new_state(self, x, y, state, old_x, old_y):
        tmp = State([state.nCols, state.nRows], (x, y),0)
        tmp.grid = [x[:] for x in state.grid]
        tmp.grid[old_x][old_y] = u"\u265E"
        tmp.grid[x][y] = u"\u2658"
        return tmp
    ###############


# State class #
###############

class State:
    def __init__(self, shape, init_pos, bool=True):
        self.nCols = shape[0]
        self.nRows = shape[1]
        self.pos_init = init_pos
        self.grid = []
        if bool:
            for i in range(self.nRows):
                self.grid.append([" "] * self.nCols)
            self.grid[init_pos[0]][init_pos[1]] = "♘"

    def get_white(self):
        return self.pos_init[0], self.pos_init[1]

    def print_grid(self):
        print('\n')
        for i in self.grid:
            print(i)

    def __str__(self):
        nsharp = (2 * self.nCols) + (self.nCols // 5)
        s = "#" * nsharp
        s += "\n"
        for i in range(self.nRows):
            s = s + "#"
            for j in range(self.nCols):
                s = s + str(self.grid[i][j]) + " "
            s = s[:-1]
            s = s + "#"
            if i < self.nRows - 1:
                s = s + '\n'
        s += "\n"
        s += "#" * nsharp
        return s

    def __eq__(self, other):
        return self.grid == other.grid

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.nCols, self.nRows, tuple(map(tuple, self.grid))))


##############################
# Launch the search in local #
##############################
# Use this block to test your code in local
# Comment it and uncomment the next one if you want to submit your code on INGInious
with open('instances.txt') as f:
    instances = f.read().splitlines()

for instance in instances:
    elts = instance.split(" ")
    shape = (int(elts[0]), int(elts[1]))
    init_pos = (int(elts[2]), int(elts[3]))
    init_state = State(shape, init_pos)

    problem = Knight(init_state)

    # example of bfs graph search
    startTime = time.perf_counter()
    node, nbExploredNodes = depth_first_graph_search(problem)
    endTime = time.perf_counter()

    # example of print
    path = node.path()
    path.reverse()

    print('Number of moves: ' + str(node.depth))
    for n in path:
        print(n.state)  # assuming that the __str__ function of state outputs the correct format
        print()
    print("nb nodes explored = ", nbExploredNodes)
    print("time : " + str(endTime - startTime))

"""
####################################
# Launch the search for INGInious  #
####################################
# Use this block to test your code on INGInious
shape = (int(sys.argv[1]), int(sys.argv[2]))
init_pos = (int(sys.argv[3]), int(sys.argv[4]))
init_state = State(shape, init_pos)

problem = Knight(init_state)

# example of bfs graph search
startTime = time.perf_counter()
node, nbExploredNodes = depth_first_graph_search(problem)
endTime = time.perf_counter()

# example of print
path = node.path()
path.reverse()

print('Number of moves: ' + str(node.depth))
for n in path:
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()
print("nb nodes explored = ", nbExploredNodes)
print("time : " + str(endTime - startTime))
"""
