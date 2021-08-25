"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
nX = 0
nO = 0
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
    nX = 0
    nO = 0
    for i in board:
        for j in i:
            if j == X:
                nX += 1
            elif j == O:
                nO += 1
    if nX == 0 or nX == nO: return X
    else: return O 


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    i = 0
    IndexPosList=[]
    while i < 3:
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                IndexPosList.append((i,j))
        i += 1
    return(set(IndexPosList))



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] == EMPTY:
        currentPlayer = player(board)
        BoardCopy = copy.deepcopy(board)
        BoardCopy[i][j] = currentPlayer
        return BoardCopy
    else:
        raise Exception("Cell already taken")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #----------------------Horizontals---------------------
    #top
    if (board[0][0] == X and board[0][1] == X and board[0][2] == X):
        return X
    if (board[0][0] == O and board[0][1] == O and board[0][2] == O):
        return O
    #middle
    if (board[1][0] == X and board[1][1] == X and board[1][2] == X):
        return X
    if (board[1][0] == O and board[1][1] == O and board[1][2] == O):
        return O
    #bottom
    if (board[2][0] == X and board[2][1] == X and board[2][2] == X):
        return X
    if (board[2][0] == O and board[2][1] == O and board[2][2] == O):
        return O
    #-----------------------Verticals------------------------
    #left
    if (board[0][0] == X and board[1][0] == X and board[2][0] == X):
        return X
    if (board[0][0] == O and board[1][0] == O and board[2][0] == O):
        return O
    #middle
    if (board[0][1] == X and board[1][1] == X and board[2][1] == X):
        return X
    if (board[0][1] == O and board[1][1] == O and board[2][1] == O):
        return O
    #right
    if (board[0][2] == X and board[1][2] == X and board[2][2] == X):
        return X
    if (board[0][2] == O and board[1][2] == O and board[2][2] == O):
        return O
    #----------------------Diagonals-------------------------
    if (board[0][0] == X and board[1][1] == X and board[2][2] == X):
        return X
    if (board[0][0] == O and board[1][1] == O and board[2][2] == O):
        return O
    if (board[0][2] == X and board[1][1] == X and board[2][0] == X):
        return X
    if (board[0][2] == O and board[1][1] == O and board[2][0] == O):
        return O
    else:
        return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    nE = 0
    if(winner(board) == O or winner(board) == X):
        return True
    for i in board:
        for j in i:
            if j != EMPTY:
                nE += 1
    if(nE == 9):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    if winner(board) == None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        optimalVal = -1
        optimalMove = (-1,-1)
        for action in actions(board):
            moveVal = mini(result(board,action))
            if moveVal == 1:
                optimalMove = action
                break
            if moveVal > optimalVal:
                optimalMove = action
        return optimalMove
    if player(board) == O:
        optimalVal = 1
        optimalMove = (-1,-1)
        for action in actions(board):
            moveVal = maxi(result(board, action))
            if moveVal == -1:
                optimalMove = action
                break
            if moveVal < optimalVal:
                optimalMove = action
        return optimalMove

def mini(board):
    if terminal(board):
        return utility(board)
    value = 1
    for action in actions(board):
        value = min(value, maxi(result(board, action)))
        if value == -1:
            break
    return value

def maxi(board):
    if terminal(board):
        return utility(board)
    value = -1
    for action in actions(board):
        value = max(value, mini(result(board, action)))
        if value == 1:
            break
    return value