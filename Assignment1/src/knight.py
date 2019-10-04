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
        """
        Extends the method of the class Problem.
        The successors are computed as follow: given a state, we compute all the possible
        moves from the current position of the knight, and check if the successor is in a valid
        position.
        The successors are inversely proportionally to the number of valid positions when the
        knight is at that position. It is the Warnsdorff's rule
        :param state: the state of the current node, to be expanded
        :return: yields all the valid successors of the node with the state 'state', according to
                 the Warnsdorff's rule.
        """
        (x, y) = state.get_white()
        l = self.get_successor(x, y, state)
        l.sort(key=lambda t: -len(self.get_successor(t[0], t[1], state)))
        for (nx, ny) in l:
            yield ((nx, ny), self.new_state(nx, ny, state, x, y))

    def goal_test(self, state):
        """
        Extends the method of the class Problem.
        We have reached the goal if there isn't any white square on the board
        :param state: the state of the node to be checked
        :return: True if the goal is reached, False otherwise
        """
        for i in state.grid:
            if " " in i:
                return False
        return True

    def get_successor(self, x, y, state):
        """

        :param x: the current x-position of the knight on the board
        :param y: the current y-position of the knight on the board
        :param state: the state of the node to be expanded
        :return: the list of the positions on the board of all valid successors of the node
        """
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
        """
        Creates a new state, based on the current state. It copies the grid of the current state, changes the position
        of the knight, switching the color, according to the statement.
        :param x: the new x-position of the knight on the board for the new state
        :param y: the new y-position of the knight on the board for the new state
        :param state: the ancestor state
        :param old_x: the x-position of the knight on the board of the ancestor state
        :param old_y: the y-position of the knight on the board of the ancestor state
        :return: the new state
        """
        tmp = State([state.nCols, state.nRows], (x, y), False)
        tmp.grid = [x[:] for x in state.grid]
        tmp.grid[old_x][old_y] = u"\u265E"
        tmp.grid[x][y] = u"\u2658"
        return tmp
    ###############


# State class #
###############

class State:
    def __init__(self, shapes, init_position, total_creation=True):
        """
        Initialize a new state. The state is represented by its shape, a grid with
        only white squares (except for the current position of the knight) and the knight position.
        :param shapes: the shape of the board (the 's' at the end is used to avoid scope issues)
        :param init_position: the initial position of the knight on the board
        :param total_creation: this boolean is used when we want to create a new state based on an ancestor.
                        True by default. When false, it does not create a new grid, because the grid is
                        copied from the ancestor - it is just an optimization argument.
        """
        self.nCols = shapes[0]
        self.nRows = shapes[1]
        self.pos_init = init_position
        self.grid = []
        if total_creation:
            for i in range(self.nRows):
                self.grid.append([" "] * self.nCols)
            self.grid[init_position[0]][init_position[1]] = "♘"

    def get_white(self):
        """
        Gets the position of the knight on the board.
        :return: a tuple of the positions (x,y) of the knight on the board
        """
        return self.pos_init[0], self.pos_init[1]

    def print_grid(self):
        """
        Only used to debug. This function print the grid on the standard output
        :return: Nothing
        """
        print('\n')
        for i in self.grid:
            print(i)

    def __str__(self):
        """
        Given by the teaching staff.
        :return: A string representation of the map.
        """
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
        """
        The equality of states is checked by the grid. If the grids are the same (i.e. have the same values
        at the same places), then the two states are considered equivalent. We have seen that, doing the following,
        Python will understand to check the values and not the references of the grids.
        :param other: the other state to be compared with
        :return: True if the two states have the same grids, False otherwise
        """
        return self.grid == other.grid

    def __ne__(self, other):
        """
        The inverse of __eq__
        :param other: the other state to be compared with
        :return: True if the two states have different grids, True otherwise
        """
        return not (self == other)

    def __hash__(self):
        """
        Hash function, based on the shape of the grid and on the grid itself (the values inside).
        :return: A hash for the state
        """
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
