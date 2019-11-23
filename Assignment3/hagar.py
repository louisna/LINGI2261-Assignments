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

            if pawn > 0:
                friend = pawn - 1
                if state.is_pawn_returning(self.id, pawn) != state.is_pawn_returning(self.id, friend):
                    if 7 <= state.get_pawn_advancement(self.id, pawn) + state.get_pawn_advancement(self.id, friend) <= 9:
                        sum += 3
                else:
                    if state.get_pawn_advancement(self.id, pawn) - state.get_pawn_advancement(self.id, friend) <= 2:
                        sum += 3
            if pawn < 4:
                friend = pawn + 1
                if state.is_pawn_returning(self.id, pawn) != state.is_pawn_returning(self.id, friend):
                    if 7 <= state.get_pawn_advancement(self.id, pawn) + state.get_pawn_advancement(self.id, friend) <= 9:
                        sum += 3
                else:
                    if state.get_pawn_advancement(self.id, pawn) - state.get_pawn_advancement(self.id, friend) <= 2:
                        sum += 3

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

        
        if self.id == 0: #yellow
            if state.is_pawn_returning(self.id,1):
                if state.get_pawn_advancement(self.id,1) == 6 and (state.get_pawn_advancement(1-self.id,0)==7 or 1 <= state.get_pawn_advancement(1-self.id,0)<4):
                    safe = False
                elif state.get_pawn_advancement(self.id,1) == 7 and (state.get_pawn_advancement(1-self.id,1)==6 or state.get_pawn_advancement(1-self.id,1)==3):
                    safe = False
                elif state.get_pawn_advancement(self.id,1) == 8 and (state.get_pawn_advancement(1-self.id,2)==6 or 2 <= state.get_pawn_advancement(1-self.id,2)<4):
                    safe = False
                elif state.get_pawn_advancement(self.id,1) == 9 and (state.get_pawn_advancement(1-self.id,3)==6 or state.get_pawn_advancement(1-self.id,3)==3):
                    safe = False
                elif state.get_pawn_advancement(self.id,1) == 10 and (state.get_pawn_advancement(1-self.id,4)==7 or 1 <= state.get_pawn_advancement(1-self.id,4)<4):
                    safe = False
                if safe:
                    sum += (state.get_pawn_advancement(self.id,1)%6)*2
            if state.is_pawn_returning(self.id,3):
                if state.get_pawn_advancement(self.id,3) == 6 and (state.get_pawn_advancement(1-self.id,0)==0 or state.get_pawn_advancement(1-self.id,0)==9):
                    safe = False
                elif state.get_pawn_advancement(self.id,3) == 7 and (state.get_pawn_advancement(1-self.id,1)==1 or 7 <= state.get_pawn_advancement(1-self.id,1)<10):
                    safe = False
                elif state.get_pawn_advancement(self.id,3) == 8 and (state.get_pawn_advancement(1-self.id,2)==0 or 8 <= state.get_pawn_advancement(1-self.id,2)<10):
                    safe = False
                elif state.get_pawn_advancement(self.id,3) == 9 and (state.get_pawn_advancement(1-self.id,3)==1 or 7 <= state.get_pawn_advancement(1-self.id,3)<10):
                    safe = False
                elif state.get_pawn_advancement(self.id,3) == 10 and (state.get_pawn_advancement(1-self.id,4)==0 or state.get_pawn_advancement(1-self.id,4)==9):
                    safe = False
                if safe:
                    sum += (state.get_pawn_advancement(self.id,3)%6)*2
            if not state.is_pawn_returning(self.id,0):#left pawn
                safe = True
                if state.get_pawn_advancement(self.id,0) == 0 and (2 <= state.get_pawn_advancement(1-self.id,0)<5 or state.get_pawn_advancement(1-self.id,0)==6):
                    safe = False
                elif state.get_pawn_advancement(self.id,0) == 1 and (state.get_pawn_advancement(1-self.id,1)==4 or state.get_pawn_advancement(1-self.id,1)==6):
                    safe = False  
                elif state.get_pawn_advancement(self.id,0) == 2 and (3 <= state.get_pawn_advancement(1-self.id,2)<5 or state.get_pawn_advancement(1-self.id,2)==6):
                    safe = False  
                elif state.get_pawn_advancement(self.id,0) == 3 and (state.get_pawn_advancement(1-self.id,3)==4 or state.get_pawn_advancement(1-self.id,3)==6):
                    safe = False 
                elif state.get_pawn_advancement(self.id,0) == 4 and (2 <= state.get_pawn_advancement(1-self.id,4)<5 or state.get_pawn_advancement(1-self.id,4)==6):
                    safe = False
                if safe:
                    sum += (state.get_pawn_advancement(self.id,0)%6)*2
            if not state.is_pawn_finished(self.id,4):#right pawn
                safe = True
                if state.get_pawn_advancement(self.id,4) == 0 and (state.get_pawn_advancement(1-self.id,0) == 10 or state.get_pawn_advancement(1-self.id,0)==0):
                    safe = False
                elif state.get_pawn_advancement(self.id,4) == 1 and (8 <= state.get_pawn_advancement(1-self.id,1)<11 or state.get_pawn_advancement(1-self.id,1)==0):
                    safe = False
                elif state.get_pawn_advancement(self.id,4) == 2 and (9 <= state.get_pawn_advancement(1-self.id,2)<11 or state.get_pawn_advancement(1-self.id,2)==0):
                    safe = False  
                elif state.get_pawn_advancement(self.id,4) == 3 and (8 <= state.get_pawn_advancement(1-self.id,3)<11 or state.get_pawn_advancement(1-self.id,3)==0):
                    safe = False
                elif state.get_pawn_advancement(self.id,4) == 4 and (state.get_pawn_advancement(1-self.id,4) == 10 or state.get_pawn_advancement(1-self.id,4)==0):
                    safe = False
                if safe:
                    sum += (state.get_pawn_advancement(self.id,4)%6)*2
        else: #red
            if state.is_pawn_returning(self.id,4):#bottom pawn
                safe = True
                if state.get_pawn_advancement(self.id,4) == 6 and (8 <= state.get_pawn_advancement(1-self.id,0)<11  or state.get_pawn_advancement(1-self.id,0)==0):
                    safe = False
                elif state.get_pawn_advancement(self.id,4) == 7 and (state.get_pawn_advancement(1-self.id,1) == 10 or state.get_pawn_advancement(1-self.id,1)==0):
                    safe = False
                elif state.get_pawn_advancement(self.id,4) == 8 and (9 <= state.get_pawn_advancement(1-self.id,2)<11 or state.get_pawn_advancement(1-self.id,2)==0):
                    safe = False  
                elif state.get_pawn_advancement(self.id,4) == 9 and (state.get_pawn_advancement(1-self.id,3) == 10 or state.get_pawn_advancement(1-self.id,3)==0):
                    safe = False
                elif state.get_pawn_advancement(self.id,4) == 10 and (8 <= state.get_pawn_advancement(1-self.id,4)<11 or state.get_pawn_advancement(1-self.id,4)==0):
                    safe = False
                if safe:
                    sum += (state.get_pawn_advancement(self.id,4)%6)*2
            if state.is_pawn_returning(self.id,0):#toppest pawn
                safe = True
                if state.get_pawn_advancement(self.id,0) == 6 and (state.get_pawn_advancement(1-self.id,0)==4 or state.get_pawn_advancement(1-self.id,0)==6):
                    safe = False
                elif state.get_pawn_advancement(self.id,0) == 7 and (2 <= state.get_pawn_advancement(1-self.id,1)<5 or state.get_pawn_advancement(1-self.id,1)==6):
                    safe = False  
                elif state.get_pawn_advancement(self.id,0) == 8 and (3 <= state.get_pawn_advancement(1-self.id,2)<5 or state.get_pawn_advancement(1-self.id,2)==6):
                    safe = False  
                elif state.get_pawn_advancement(self.id,0) == 9 and (2 <= state.get_pawn_advancement(1-self.id,3)<5 or state.get_pawn_advancement(1-self.id,3)==6):
                    safe = False 
                elif state.get_pawn_advancement(self.id,0) == 10 and (state.get_pawn_advancement(1-self.id,4)==4 or state.get_pawn_advancement(1-self.id,4)==6):
                    safe = False
                if safe:
                    sum += (state.get_pawn_advancement(self.id,0)%6)*2
            if not state.is_pawn_returning(self.id,1):
                safe = True
                if state.get_pawn_advancement(self.id,1) == 0 and (state.get_pawn_advancement(1-self.id,4)==6 or state.get_pawn_advancement(1-self.id,4)==3):
                    safe = False
                elif state.get_pawn_advancement(self.id,1) == 1 and (state.get_pawn_advancement(1-self.id,3)==7 or 1 <= state.get_pawn_advancement(1-self.id,3)<4):
                    safe = False
                elif state.get_pawn_advancement(self.id,1) == 2 and (state.get_pawn_advancement(1-self.id,2)==6 or 2 <= state.get_pawn_advancement(1-self.id,2)<4):
                    safe = False
                elif state.get_pawn_advancement(self.id,1) == 3 and (state.get_pawn_advancement(1-self.id,1)==7 or 1 <= state.get_pawn_advancement(1-self.id,1)<4):
                    safe = False
                elif state.get_pawn_advancement(self.id,1) == 4 and (state.get_pawn_advancement(1-self.id,0)==6 or state.get_pawn_advancement(1-self.id,0)==3):
                    safe = False
                if safe:
                    sum += (state.get_pawn_advancement(self.id,1)%6)*2
            if not state.is_pawn_finished(self.id,3):
                safe = True
                if state.get_pawn_advancement(self.id,3) == 0 and (state.get_pawn_advancement(1-self.id,4)==1 or 7 <= state.get_pawn_advancement(1-self.id,4)<10):
                    safe = False
                elif state.get_pawn_advancement(self.id,3) == 1 and (state.get_pawn_advancement(1-self.id,3)==0 or state.get_pawn_advancement(1-self.id,3)==9):
                    safe = False
                elif state.get_pawn_advancement(self.id,3) == 2 and (state.get_pawn_advancement(1-self.id,2)==0 or 8 <= state.get_pawn_advancement(1-self.id,2)<10):
                    safe = False
                elif state.get_pawn_advancement(self.id,3) == 3 and (state.get_pawn_advancement(1-self.id,1)==0 or state.get_pawn_advancement(1-self.id,1)==9):
                    safe = False
                elif state.get_pawn_advancement(self.id,3) == 4 and (state.get_pawn_advancement(1-self.id,0)==1 or 7 <= state.get_pawn_advancement(1-self.id,0)<10):
                    safe = False
                if safe:
                    sum += (state.get_pawn_advancement(self.id,3)%6)*2

        return sum
