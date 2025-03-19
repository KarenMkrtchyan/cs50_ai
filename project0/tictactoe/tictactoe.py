"""
Tic Tac Toe Player
"""

import math
import copy

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
    x_count = 0
    o_count = 0
    for row in board:
        for col in row:
            if col == X:
                x_count+=1
            elif col == O:
                o_count+=1
    return X if o_count==x_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == EMPTY:
                    actions.append((row,col))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY or action[0]>2 or action[1]>2:
        raise ImportError('not a valid action')
    
    who = player(board)
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = who
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[0][1] and board[0][1] == board[0][2] and board[0][0] != EMPTY:
        return X if board[0][0] == X else O
    if board[1][0] == board[1][1] and board[1][1] == board[1][2] and board[1][0] != EMPTY:
        return X if board[1][0] == X else O
    if board[2][0] == board[2][1] and board[2][1] == board[2][2] and board[2][0] != EMPTY:
        return X if board[2][0] == X else O
  
    if board[0][0] == board[1][0] and board[1][0] == board[2][0] and board[0][0] != EMPTY:
        return X if board[0][0] == X else O
    if board[0][1] == board[1][1] and board[1][1] == board[2][1] and board[0][1] != EMPTY:
        return X if board[0][1] == X else O
    if board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[0][2] != EMPTY:
        return X if board[0][2] == X else O

    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return X if board[0][0] == X else O
    if board[2][0] == board[1][1] and board[1][1] == board[0][2] and board[2][0] != EMPTY:
        return X if board[2][0] == X else O
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == None and (EMPTY in board[0] or EMPTY in board[1] or EMPTY in board[2]): # there are potentially betters ways of doing this 
        return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0

def max_value(board):
    if(terminal(board)):
        return utility(board)
    
    list_action = actions(board)
    v = -10
    for action in list_action:
        v = max(v, min_value(result(board, action)))
    return v 

            
def min_value(board):
    if(terminal(board)):
        return utility(board)

    list_action = actions(board)
    v = 10
    for action in list_action: 
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    who = player(board)
    if who == X:
        list_action = actions(board)
        best_action = list_action[0]
        best_eval = -10
        for action in list_action:
            eval =  min_value(result(board, action)) 
            if eval > best_eval:
                best_eval = eval
                best_action = action
        return best_action
    
    if who == O:
        list_action = actions(board)
        best_action = list_action[0]
        best_eval = 10
        for action in list_action:
            eval =  max_value(result(board, action)) 
            if eval < best_eval:
                best_eval = eval
                best_action = action
        return best_action
                
       

