from agent import AlphaBetaAgent
import minimax

"""
Agent skeleton. Fill in the gaps.
"""


class MyAgent(AlphaBetaAgent):

    """
    This is the skeleton of an agent to play the Squadro game.
    """
    def get_action(self, state, last_action, time_left):
        self.last_action = last_action
        self.time_left = time_left
        return minimax.search(state, self)

    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """
    def successors(self, state):
        actions = state.get_current_player_actions()
        for a in actions:
            new_state = state.copy()
            new_state.apply_action(a)
            yield a, new_state

    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state, depth):
        if state.game_over_check():
            return True
        return depth >= 1  # arbitrary set max depth to 1

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """
    def evaluate(self, state):
        sum = 0
        for pawn in range(5):  # they are 5 pawn
            sum += state.get_pawn_advancement(self.id, pawn)
        return sum