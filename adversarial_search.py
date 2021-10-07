############################################################
# CIS 521: adversarial_search
############################################################

student_name = "Jingyi Lu"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import collections
import copy
import itertools
import random
import math

############################################################
# Section 1: Dominoes Game
############################################################
def create_dominoes_game(rows, cols):
    board = [[False for c in range(cols)] for r in range(rows)]
    newDomi = DominoesGame(board)
    return newDomi

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        
    def get_board(self):
        return self.board

    def reset(self):
        self.board = [[False] * self.cols for r in range(self.rows)]

    def is_legal_move(self, row, col, vertical):
        if row == self.rows - 1 and vertical:
            return False
        if col == self.cols - 1 and not vertical:
            return False
        if self.board[row][col] == True:
            return False
        elif not vertical and self.board[row][col+1] == True:
            return False
        elif vertical and self.board[row+1][col] == True:
            return False
        return True

    def legal_moves(self, vertical):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_legal_move(row, col, vertical):
                    yield (row, col)

        
    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row, col, vertical):
            self.board[row][col] = True
            if vertical:
                self.board[row+1][col] = True
            else:
                self.board[row][col+1] = True
        

    def game_over(self, vertical):
        moves = list(self.legal_moves(vertical))
        if len(moves) == 0:
            return True
        else:
            return False

    def copy(self):
        new_board = copy.deepcopy(self.board)
        return DominoesGame(new_board)

    def successors(self, vertical):
        for (row, col) in self.legal_moves(vertical):
            new_game = self.copy()
            new_game.perform_move(row, col, vertical)
            yield ((row, col), new_game)

    def get_random_move(self, vertical):
        moves = list(self.legal_moves(vertical))
        return random.choice(moves)
    
    def evaluate(self, vertical):
        our = list(self.legal_moves(vertical))
        their = list(self.legal_moves(not vertical))
        return  len(our) - len(their)

    def max_value(self, vertical, limit, alpha, beta):
        if (limit ==  0 or self.game_over(vertical)):
            return (None, self.evaluate(vertical), 1)
        
        v = -float('inf')
        num_leaves = 0
        best_move = [-1, -1]
        for (new_move, new_game) in self.successors(vertical):
            (child_move, new_v, child_leaves) =  new_game.min_value(not vertical, limit - 1, alpha, beta)
            if v < new_v:
                best_move = new_move
                v = new_v
            num_leaves += child_leaves
            
            if  v >= beta:
                return (tuple(best_move), v, num_leaves)
            alpha = max(alpha, v)
            
        return (tuple(best_move), v, num_leaves)

    def min_value(self, vertical, limit, alpha, beta):
        if (limit == 0 or self.game_over(vertical)):
            return (None, self.evaluate(not vertical), 1)
        v = float('inf')
        num_leaves = 0
        for (new_move, new_game) in self.successors(vertical):
            (child_move, new_v, child_leaves) = new_game.max_value(not vertical, limit - 1, alpha, beta)
            
            v = min(v, new_v)
            num_leaves += child_leaves
            
            if v <= alpha:
                return ((), v, num_leaves)
            beta = min(beta, v)
            
        return ((), v, num_leaves)
            
        
    # Required
    def get_best_move(self, vertical, limit):
        return self.max_value(vertical, limit, -float('inf'), float('inf'))
        
    
############################################################

feedback_question_1 = 8

feedback_question_2 = """
It takes me some time to understand alpha-beta search
"""

feedback_question_3 = """
The game is fun
"""
