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
        goto = [(0,0), (1,0),(-1,0),(0,1),(0,-1)]
        li = []
        for xp,yp in state.pacmenPos :
            lp = []
            for x,y in goto:
                if self.validePos(state, (xp + x, yp + y)):
                    lp.append((x, y))
            li.append(lp)
        prod = list(itertools.product(*li))
        l = tuple([(0, 0) for i in range(len(state.pacmenPos))])
        prod.remove(l)
        for act in prod :
            boo = True
            new_positions = []
            grid = [x[:] for x in state.grid]
            for i in range(len(state.pacmenPos)):
                x,y = state.pacmenPos[i]
                ax,ay = act[i]
                nx, ny = x+ax, y+ay
                if (x,y) not in new_positions:
                    grid[x][y] = " "
                if (nx, ny) in new_positions :# or (nx, ny) in state.pacmenPos:
                    boo = False
                    break
                else:
                    new_positions.append((nx, ny))
                grid[nx][ny] = "$"
            if boo:
                new_state = State(grid)
                yield (act, new_state)

    """
    def successor(self, state):
        goto = [ (1, 0), (-1, 0), (0, -1), (0, -1)]
        l = []
        for x, y in goto:
            if self.validePos(state, (x+state.pacmenPos[0][0], y+state.pacmenPos[0][1])):
                l.append((x,y))
        for x,y in l:
            grid = [i[:] for i in state.grid]
            grid[state.pacmenPos[0][0]][state.pacmenPos[0][1]] = " "
            grid[x+state.pacmenPos[0][0]][y+state.pacmenPos[0][1]] = "$"
            news = State(grid)
            yield  ((x,y), news)
    """





    def validePos(self, state, pos):
        (x,y) = pos
        return 0 <= x < state.nbr and 0 <= y < state.nbc and state.grid[x][y] != "x"

    def goal_test(self, state):
        for i in state.grid:
            if "@" in i:
                return False
        return True

    """
    def path_cost(self, c, state1, action, state2):
        """"""Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path.""""""
        return c + len(action) - list(action).count((0,0))
        #return c + 1  # recal avec le nombre de pacmen ayant bougé
        """



###############
# State class #
###############
class State:

    def __init__(self, grid):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.pacmenPos = []  # list des pacmen
        self.food = []  # list de la nourriture restante
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
        return self.grid == other_state.grid

    def __hash__(self):
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
def heuristic(node):
    if len(node.state.food) == 0:
        return 0
    distMM = 0
    for (x, y) in node.state.pacmenPos:
        distMin = 999999999999999
        for (xf, yf) in node.state.food:
            if distMin > abs(x-xf) + abs(y-yf):
                distMin = abs(x-xf) + abs(y-yf)
        distMM += distMin

    return distMM


#####################
# Launch the search #
#####################
grid_init = readInstanceFile(sys.argv[1])
init_state = State(grid_init)
#print(init_state)

problem = Pacmen(init_state)

startTime = time.perf_counter()
node, nbExploredNodes = astar_graph_search(problem, heuristic)
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
