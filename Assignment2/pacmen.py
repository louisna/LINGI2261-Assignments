# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gael Aglin <gael.aglin@uclouvain.be>'''
import time
from search import *
import itertools


#################
# Problem class #
#################
class Pacmen(Problem):

    def successor(self, state):
        """
        Extends the method of the class Problem.
        The successors are computed as follow: given a state, we compute all the possible
        moves from the current position of the pacmen, and check if the successor is in a valid
        position.
        We compute the possible next state of each pacman, and then make a product of these to have all the possible
        successors of the current state. We remove the possibility that each pacman stays at his place
        :param state: the state of the current node, to be expanded
        :return: yields all the valid successors of the node with the state 'state'
        """

        """
        Making this variable False will disable the possibility for any pacman to stay at his place.
        Its gives a big time improvement, even if it does not fully match the statement (the result is still correct)
        """
        can_stay = True

        if can_stay:
            goto = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]
        else:
            goto = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # li is a list, where each element is a list of possible actions for a pacman
        li = [[(x, y) for (x, y) in goto if self.validePos(state, (xp + x, yp + y))] for (xp, yp) in state.pacmenPos]
        prod = list(itertools.product(*li))

        if can_stay:  # If a pacman can stay at his place, we remove the possibility of nobody moving
            l = tuple([(0, 0) for i in range(len(state.pacmenPos))])
            prod.remove(l)

        for act in prod:
            boo = True
            new_positions = []
            grid = [x[:] for x in state.grid]
            for i in range(len(state.pacmenPos)):
                x,y = state.pacmenPos[i]
                ax,ay = act[i]
                nx, ny = x+ax, y+ay
                if (x, y) not in new_positions: # If the current position of the pacman is not a new position
                    # Then we erase the current position from the grid. Otherwise, we keep the $ symbol
                    grid[x][y] = " "
                if (nx, ny) in new_positions:  # If two pacmen move towards the same position
                    boo = False  # We break both for-loops, because it is not a valid successor
                    break
                else:
                    new_positions.append((nx, ny))  # Append the new position
                grid[nx][ny] = "$"
            if boo:  # If it is a valid state
                new_state = State(grid)
                yield (act, new_state)

    def validePos(self, state, pos):
        """
        Check if the position given by 'pos' is valid in the sens that it is a movement inside the grid,
        and it is not a wall
        :param state: the current state
        :param pos: the new position to be checked
        :return: True if the position is valid, False otherwise
        """
        (x, y) = pos
        return 0 <= x < state.nbr and 0 <= y < state.nbc and state.grid[x][y] != "x"

    def goal_test(self, state):
        """
        Extends the method of the class Problem.
        The goal is reached if there is no food on the board given by 'state'
        :param state: the current state
        :return: True if the goal is reached (no food on the board), False otherwise
        """
        for i in state.grid:
            if "@" in i:
                return False
        return True


###############
# State class #
###############

class State:

    def __init__(self, grid):
        """
        Initialize a new state. The state is represented by its shape, a grid with the initial positions of the
        pacmen, and the foods.
        The coordinates of the pacmen and of the foods are kept in list to easier the retrieve of information.
        :param grid: The grid containing all the information about the location of the walls, the pacmen and the foods.
        """
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.pacmenPos = []  # list of all pacmen
        self.food = []  # list of all the foods on the board, given by 'grid'
        for x in range(self.nbr):
            for y in range(self.nbc):
                if grid[x][y] == "$":
                    self.pacmenPos.append((x, y))
                elif grid[x][y] == "@":
                    self.food.append((x, y))

    def __str__(self):
        nsharp = self.nbc * 2 + 3
        s = "#" * nsharp
        s += '\n'
        for i in range(0, self.nbr):
            s += "# "
            for j in range(0, self.nbc):
                s += str(self.grid[i][j]) + " "
            s += "#"
            if i < self.nbr:
                s += '\n'
        s += "#" * nsharp
        return s

    def __eq__(self, other_state):
        """
        The equality of states is checked by the grid. If the grids are the same (i.e. have the same values
        at the same places), then the two states are considered equivalent. We have seen that, doing the following,
        Python will understand to check the values and not the references of the grids.
        :param other_state: the other state to be compared with
        :return: True if the two states have the same grids, False otherwise
        """
        return self.grid == other_state.grid

    def __hash__(self):
        """
        Hash function, based on the shape of the grid and on the grid itself (the values inside).
        :return: A hash for the state
        """
        return hash(tuple(map(tuple, self.grid)))


######################
# Auxiliary function #
######################
def readInstanceFile(filename):
    lines = [[char for char in line.rstrip('\n')[1:][:-1]] for line in open(filename)]
    lines = lines[1:len(lines) - 1]
    n = len(lines)
    m = len(lines[0])
    grid_init = [[lines[i][j] for j in range(1, m, 2)] for i in range(0, n)]
    return grid_init


######################
# Heuristic function #
######################
def heuristic_2(node):
    """
    Heuristic uses a 'Manhattan distance' approach. For each food, it computes the minimum
    'Manhattan distance' towards the pacmen, and returns the maximum of these minimum 'Manhattan distances'.
    :param node: The node to be processed
    :return: the maximum of the minimum 'Manhattan distance' computed for each food between the food and the
             nearest pacman.
    """
    if len(node.state.food) == 0:  # If there is no food, the heuristic returns 0
        return 0
    distMM = 0
    for (xf, yf) in node.state.food:
        distMin = 999999999999999 # To be sure that we get a valid distance
        for (x, y) in node.state.pacmenPos:
            if distMin > abs(x-xf) + abs(y-yf):
                distMin = abs(x-xf) + abs(y-yf)
        distMM = max(distMM, distMin) # We keep the biggest minimum 'Manhattan distance' for each food

    return distMM


def valide_pos(state, pos, map):
    """
    Used in the below heuristic
    Check if the position 'pos' is valid. The position is valid if it is in the grid, has not been visited yet,
    and if it is not a wall (both conditions are directly verified if the value is not 'x'.
    :param state: The state to be processed
    :param pos: the position to be checked
    :param map: the current map
    :return: True if the position is valid, False otherwise
    """
    (x,y) = pos
    return 0 <= x < state.nbr and 0 <= y < state.nbc and map[x][y] != "x"

def heuristic(node):
    """
    Heuristic using a 'breadth-first' search approach. We start the BFS with all the pacmen as sources. Then
    we look for the shortest path towards each food (once a food is reached by a pacman, this food is considered as
    visited). Then the heuristic returns the biggest shortest path computed by the BFS.
    It uses the class Queue.
    :param node: The node to be processed
    :return: the maximum of the minimum shortest path computed for each food.
    """
    food = node.state.food
    if len(food) == 0:
        return 0

    q = FIFOQueue()  # Create the FIFO-Queue
    for i in node.state.pacmenPos:  # Append all the pacmen as source, i.e., with initial distance 0
        q.append((i, 0))

    map = [x[:] for x in node.state.grid]  # We copy the grid for the process,

    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # The possible moves

    total = 0  # The value to be returned

    while len(q) > 0:
        ((x, y), cost) = q.pop()
        for (a, b) in moves:
            if valide_pos(node.state, (x+a, y+b), map):
                if map[x+a][y+b] == "@":  # A food it is !
                    total = max(total, cost)  # Getting the maximum
                map[x+a][y+b] = "x"  # Each visited location is replaced, as it is a wall
                q.append(((x+a, y+b), cost+1))  # Increment the total cost by 1
    return total

###############
# Class Queue #
###############
"""
This code comes from https://stackoverflow.com/questions/45688871/implementing-an-efficient-queue-in-python
and has a bit been modified to meet the expectations
"""
from collections import deque

class Queue():
    '''
    Thread-safe, memory-efficient, maximally-sized queue supporting queueing and
    dequeueing in worst-case O(1) time.
    '''


    def __init__(self, max_size = 100000):
        '''
        Initialize this queue to the empty queue.

        Parameters
        ----------
        max_size : int
            Maximum number of items contained in this queue. Defaults to 10.
        '''

        self._queue = deque(maxlen=max_size)
        self.size = 0


    def enqueue(self, item):
        '''
        Queues the passed item (i.e., pushes this item onto the tail of this
        queue).

        If this queue is already full, the item at the head of this queue
        is silently removed from this queue *before* the passed item is
        queued.
        '''

        self._queue.append(item)
        self.size += 1


    def dequeue(self):
        '''
        Dequeues (i.e., removes) the item at the head of this queue *and*
        returns this item.

        Raises
        ----------
        IndexError
            If this queue is empty.
        '''
        self.size -= 1
        return self._queue.pop()

#####################
# Launch the search #
#####################
grid_init = readInstanceFile(sys.argv[1])
init_state = State(grid_init)
#print(init_state)

problem = Pacmen(init_state)

startTime = time.perf_counter()
#node, nbExploredNodes = astar_graph_search(problem, heuristic)
node, nbExploredNodes = breadth_first_graph_search(problem)
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
