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
    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    Xs = 0
    Os = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                Xs += 1
            elif board[i][j] == O:
                Os += 1
    return X if Xs == Os else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available_action = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                available_action.add((i, j))
    return available_action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if i > 2 or i < 0 or j > 2 or j < 0 or board[i][j] != EMPTY:
        raise Exception("Invalid move")

    result_board = [row[:] for row in board]
    result_board[i][j] = player(board)
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winning_positions = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(2, 0), (1, 1), (0, 2)],
    ]
    for player in [X, O]:
        for winning_pos in winning_positions:
            player_wins = True
            for cell in winning_pos:
                i, j = cell
                if board[i][j] != player:
                    player_wins = False
                    break
            if player_wins:
                return player
    return EMPTY


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) in [X, O]:
        return True
    empties = 0
    for i in range(len(board)):
        if empties != 0:
            break
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                empties = 1
                break
    return empties == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    player = winner(board)
    if player == X:
        return 1
    elif player == O:
        return -1
    else:
        return 0


def min_value(board):
    if terminal(board):
        return utility(board)
    value = math.inf
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    return value


def max_value(board):
    if terminal(board):
        return utility(board)
    value = -math.inf
    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    return value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)
    if current_player == X:
        # choose the action that produces the highest value of Min-Value(a)
        highest_value = -math.inf
        highest_action = None
        for action in actions(board):
            result_board = result(board, action)
            result_value = min_value(result_board)
            if result_value > highest_value:
                highest_value = result_value
                highest_action = action
        return highest_action
    else:
        # choose the action that produces the lowers value of the Max-Value(a)
        lowest_value = math.inf
        lowest_action = None
        for action in actions(board):
            result_board = result(board, action)
            result_value = max_value(result_board)
            if result_value < lowest_value:
                lowest_value = result_value
                lowest_action = action
        return lowest_action
