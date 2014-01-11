from random import choice
import numpy as np

combo_indices = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]

EMPTY_SIGN = '.'
AI_SIGN = 'X'
OPPONENT_SIGN = 'O'

# print board
def print_board(board):
    print(" ")
    print(' '.join(board[:3]))
    print(' '.join(board[3:6]))
    print(' '.join(board[6:]))
    print(" ")
    
# human player
def opponent_move(board, row, column):
    index = 3 * (row - 1) + (column - 1)
    if board[index] == EMPTY_SIGN:
        return board[:index] + OPPONENT_SIGN + board[index + 1:]
    return board

# find best move
def best_moves_from_board(board, sign):
    move_list = []
    utilities = utility_matrix(board)
    max_utility = max(utilities)
    for i, v in enumerate(board):
        if utilities[i] == max_utility:
            move_list.append(board[:i] + sign + board[i + 1:])
    return move_list

# all moves
def all_moves_from_board(board, sign):
    move_list = []
    for i, v in enumerate(board):
        if v == EMPTY_SIGN:
            new_board = board[:i] + sign + board[i + 1:]
            move_list.append(new_board)
            if game_won_by(new_board) == AI_SIGN:
                return [new_board]
    return move_list

# all moves from list
def all_moves_from_board_list(board_list, sign):
    move_list = []
    get_moves = best_moves_from_board if sign == AI_SIGN else all_moves_from_board
    for board in board_list:
        move_list.extend(get_moves(board, sign))
    return move_list

# ai player
def ai_move(board):
    new_boards = all_moves_from_board(board, AI_SIGN)
    for new_board in new_boards:
        if game_won_by(new_board) == AI_SIGN:
            return new_board
    return choice(new_boards)

# game winner
def game_won_by(board):
    for index in combo_indices:
        if board[index[0]] == board[index[1]] == board[index[2]] != EMPTY_SIGN:
            return board[index[0]]
    return EMPTY_SIGN

def init_utility_matrix(board):
    return [0 if cell == EMPTY_SIGN else -1 for cell in board]

def generate_add_score(utilities, i, j, k):
    def add_score(points):
        if utilities[i] >= 0:
            utilities[i] += points
        if utilities[j] >= 0:
            utilities[j] += points
        if utilities[k] >= 0:
            utilities[k] += points
    return add_score

def utility_matrix(board):
    utilities = init_utility_matrix(board)
    for [i, j, k] in combo_indices:
        add_score = generate_add_score(utilities, i, j, k)
        triple = [board[i], board[j], board[k]]
        if triple.count(EMPTY_SIGN) == 1:
            if triple.count(AI_SIGN) == 2:
                add_score(1000)
            elif triple.count(OPPONENT_SIGN) == 2:
                add_score(100)
        elif triple.count(EMPTY_SIGN) == 2 and triple.count(AI_SIGN) == 1:
            add_score(10)
        elif triple.count(EMPTY_SIGN) == 3:
            add_score(1)
    return utilities

# start game
def start_game():
    board = EMPTY_SIGN * 9
    empty_cell_count = 9
    is_game_ended = False
    while empty_cell_count > 0 and not is_game_ended:
        if empty_cell_count % 2 == 1:
            board = ai_move(board)
        else:
            row = int(input('Enter row: '))
            col = int(input("Enter column: "))
            board = opponent_move(board, row, col)
        print_board(board)
        is_game_ended = game_won_by(board) != EMPTY_SIGN
        empty_cell_count = sum(1 for cell in board if cell == EMPTY_SIGN)
    print("Game has been ended.")
    
start_game()
