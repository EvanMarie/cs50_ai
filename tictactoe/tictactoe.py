"""
Tic Tac Toe Player
"""

import math
from pyexpat.errors import XML_ERROR_RECURSIVE_ENTITY_REF
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

# Pardon the massive amounts of comments necessary to keep my brain in order.

# Height and width of board variables for all the looping
board_height = 3
board_width = 3
    
def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Variables for determining next player
    x_count = 0
    o_count = 0

    # Loop for counting Xs and Os on the board to determin next player
    for row in range(board_height):
        for column in range(board_width):
            if board[row][column] == X:
                x_count += 1
            if board[row][column] == O:
                o_count += 1 
                
    # And the next player is!
    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Available actions, empty spots, found on the game board.
    available_actions = set()

    # Loop to check for available spots to choose, to be added to available_actions
    for row in range(board_height):
        for column in range(board_width):
            if board[row][column] == EMPTY:
                available_actions.add((row, column))

    return available_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check to see if the action is a valid move for the player
    if action not in actions(board):
        raise Exception('Invalid next move.')

    # Make deepcopy of the board as indicated in the documentation
    row, column = action
    deepcopy_board = copy.deepcopy(board)
    
    # Place current player's move on the deepcopied board
    deepcopy_board[row][column] = player(board)
    
    # Return board with player's move added
    return deepcopy_board


# Functions to determine the winner of the game, if X or O has 3 in a row in any of the 
# 3 possible directions:

def row_check_loop(board, player): 
    # Loop through rows
    for row in range(board_height):
        if (board[row][0] == player and
            board[row][1] == player and
            board[row][2] == player):
            # If 3 consecutive Xs or Os, return True, i.e. there is a winner
            return True
    # Otherwise, return False, i.e. there is no winner.
    return False
  
  
def column_check_loop(board, player):       
    # Repeating the looping used to check the rows, but this time for columns
    for column in range(board_width):
        if (board[0][column] == player and
            board[1][column] == player and
            board[2][column] == player):
            
            return True 
        
    return False
    
    
def diagonal_right_check_loop(board, player):
    # Checking diagonal starting top left

    if (board[0][0] == player and
        board[1][1] == player and
        board[2][2] == player):
        return True 
    return False

def diagonal_left_check_loop(board, player):
    # Checking diagonal starting top right

    if (board[0][2] == player and
        board[1][1] == player and
        board[2][0] == player):
        return True 
    return False    
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player in (X, O):
        if (row_check_loop(board, player) or
            column_check_loop(board, player) or
            diagonal_right_check_loop(board, player) or
            diagonal_left_check_loop(board, player)):
            return player 
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for row in range(board_height):
        for column in range(board_width):
            if board[row][column] == EMPTY:
                
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


def get_score(board, action):
    # Loop through all actions
        # For each action, play out the game to see outcome for player
    score = 0
    starting_board = result(board, action)
    # If there is no winner or tie
    if terminal(starting_board) == False:
        all_actions = actions(starting_board)
        action_count = len(all_actions)
        for action in all_actions:
            # Get score for current board
            score += get_score(starting_board, action)
        # Add score for current game judged
        score = score / action_count    
    else:
        score = utility(starting_board)
        
    return score


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """ 
    # Keep a list of final scores for each possible action
    all_scores = {}
    for action in actions(board):
        # Add the final score of based on current action to all_scores
        all_scores[action] = get_score(board, action)
        
    # If the player is X, find the best_score in all_scores to determine best action
    if player(board) == X:
        best_score = -100000
        best_action = None
        for action, score in all_scores.items():
            if score > best_score:
                best_score = score
                best_action = action           
        return best_action
    
    # If the player is O, find the best_score in all_scores to determine best action    
    if player(board) == O:
        best_score = 100000
        best_action = None
        for action, score in all_scores.items():
            if score < best_score:
                best_score = score
                best_action = action      
        return best_action