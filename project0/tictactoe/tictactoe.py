"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    result = utility(board)
    if result == -1:
        return O
    if result == 1:
        return X
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if utility(board) == 0 and None in board:
        return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if board[0,0] == board[0,1] and board[0,1] == board[0,2]:
        return 1 if board[0,0] == X else -1
    if board[1,0] == board[1,1] and board[1,1] == board[1,2]:
        return 1 if board[0,0] == X else -1
    if board[0,0] == board[2,1] and board[2,1] == board[2,2]:
        return 1 if board[0,0] == X else -1
  
    if board[0,0] == board[1,0] and board[1,0] == board[2,0]:
        return 1 if board[0,0] == X else -1
    if board[1,0] == board[1,1] and board[1,1] == board[2,1]:
        return 1 if board[0,0] == X else -1
    if board[2,0] == board[2,1] and board[2,2] == board[2,2]:
        return 1 if board[0,0] == X else -1

    if board[0,0] == board[1,1] and board[1,1] == board[2,2]:
        return 1 if board[0,0] == X else -1
    if board[2,0] == board[1,1] and board[1,1] == board[0,2]:
        return 1 if board[0,0] == X else -1

    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
