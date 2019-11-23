from agent import AlphaBetaAgent
import minimax
import squadro_state

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
        self.count = 0
        for pawn in range(5):
            if state.is_pawn_finished(self.id,pawn):
                self.count += 1
            if state.is_pawn_finished(1-self.id,pawn):
                self.count += 1
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
        return depth >= 5 + self.count # arbitrary set max depth to 1

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """
    def evaluate(self, state):
        sum = 0
        count = 0
        if state.game_over_check() and state.get_winner() == self.id:
            return 1000000
        elif state.game_over_check() and state.get_winner() == 1 - self.id:
            return -1000000
        for pawn in range(5):
            if state.is_pawn_returning(self.id, pawn):
                count += 1

            if state.is_pawn_returning(self.id, pawn):
                sum += squadro_state.MOVES_RETURN[self.id][pawn]

            if state.is_pawn_finished(self.id, pawn):
                sum += 8

            new_state2 = state.copy()
            new_state2.cur_player = 1-self.id
            if new_state2.is_action_valid(pawn):
                new_state2.move_1(1-self.id, pawn) # A CHANGER
                if new_state2.check_crossings(1-self.id,pawn):
                    advancement = new_state2.get_pawn_advancement(self.id, pawn)
                    if new_state2.is_pawn_returning(self.id, pawn):
                        speed = squadro_state.MOVES_RETURN[self.id][pawn]
                    else:
                        speed = squadro_state.MOVES[self.id][pawn]
                    sum -= round((advancement % 6)/speed)

            sum += (state.get_pawn_advancement(self.id, pawn) - state.get_pawn_advancement(1-self.id, pawn)) * 2

        if count == 4:
            sum += 5

        state_copy = state.copy()
        state_copy.cur_player = 1 - self.id
        adv_actions = state_copy.get_current_player_actions()  # All the actions of the opponent
        for action in adv_actions:
            state_intern = state_copy.copy()
            state_intern.apply_action(action)
            for pawn in range(5):
                state_intern.move_1(self.id, pawn)
                if state_intern.check_crossings(self.id, pawn):
                    advancement = state_intern.get_pawn_advancement(self.id, pawn)
                    if state_intern.is_pawn_returning(1-self.id, pawn):
                        speed = squadro_state.MOVES_RETURN[1-self.id][pawn]
                    else:
                        speed = squadro_state.MOVES[1-self.id][pawn]
                    sum += round((advancement % 6) / speed)

        return sum
