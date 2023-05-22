from machine import Pin
from time import sleep
from math import inf
from random import choice

from SR import SR


# Function to calculate the best move for the computer player (O)
def calculate_best_move(board):
    best_score = -inf
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':

                board[row][col] = 'O'
                score = minimax(board, False)
                board[row][col] = ' '

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    return best_move


# Minimax algorithm for determining the best move
def minimax(board, is_maximizing):
    if check_winner(board, 'X'):
        return -1
    elif check_winner(board, 'O'):
        return 1
    elif is_board_full(board):
        return 0

    best_score = -inf if is_maximizing else inf
    player = 'O' if is_maximizing else 'X'

    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':

                board[row][col] = player
                score = minimax(board, not is_maximizing)
                board[row][col] = ' '

                if is_maximizing:
                    best_score = max(score, best_score)
                else:
                    best_score = min(score, best_score)

    return best_score


# Function to check if a player has won the game
def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(row[col] == player for row in board):
            return True

    if board[0][0] == board[1][1] == board[2][2] == player:
        return True

    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False


# Function to check winning coorditates
def check_winning_coordinates(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2]:
            return [(row, i) for i in range(3)]
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            return [(i, col) for i in range(3)]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
        return [(i, i) for i in range(3)]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
        return [(i, 2-i) for i in range(3)]


# Function to check if the board is full
def is_board_full(board):
    return all(' ' not in row for row in board)


# Function to update the LED diodes based on the game board
def light_diodes():
    x_fields = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    o_fields = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                x_fields[row * 3 + col] = 1
            elif board[row][col] == 'O':
                o_fields[row * 3 + col] = 1
            elif board[row][col] == '!':
                x_fields[row * 3 + col] = 1
                o_fields[row * 3 + col] = 1

    # Update the LED diodes based on the values in x_fields and o_fields lists
    diodes_green.clear()
    number = (
        x_fields[-2] * 1
        + x_fields[-3] * 2
        + x_fields[-4] * 4
        + x_fields[-5] * 8
        + x_fields[-6] * 16
        + x_fields[-7] * 32
        + x_fields[-8] * 64
        + x_fields[-9] * 128
    )
    diodes_green.bits(number, 8, True)

    if x_fields[-1]:
        diode_8_green.value(1)
    else:
        diode_8_green.value(0)

    number = (
        o_fields[-2] * 1
        + o_fields[-3] * 2
        + o_fields[-4] * 4
        + o_fields[-5] * 8
        + o_fields[-6] * 16
        + o_fields[-7] * 32
        + o_fields[-8] * 64
        + o_fields[-9] * 128
    )
    diodes_red.bits(number, 8, True)

    if o_fields[-1]:
        diode_8_red.value(1)
    else:
        diode_8_red.value(0)


# Function to make led flash
def flash_led(coordinates):
    signs = []

    for c in coordinates:
        signs.append(board[c[0]][c[1]])

    while True:
        for c in coordinates:
            board[c[0]][c[1]] = ' '

        light_diodes()
        sleep(0.25)

        for i, c in enumerate(coordinates):
            board[c[0]][c[1]] = signs[i]

        light_diodes()
        sleep(0.25)


# Setting up pins and initializing variables
control_buttons = [
    Pin(34, Pin.IN),
    Pin(35, Pin.IN),
    Pin(32, Pin.IN),
    Pin(33, Pin.IN),
    Pin(25, Pin.IN),
    Pin(26, Pin.IN),
    Pin(27, Pin.IN),
    Pin(14, Pin.IN),
    Pin(12, Pin.IN),
]
difficulty_switch = Pin(13, Pin.IN)

DS1 = Pin(23, Pin.OUT)
SHCP1 = Pin(19, Pin.OUT)
STCP = Pin(21, Pin.OUT)
MR = Pin(18, Pin.OUT, value=1)
OE = Pin(22, Pin.OUT, value=0)

DS2 = Pin(5, Pin.OUT)
SHCP2 = Pin(15, Pin.OUT)

diodes_red = SR(DS1, SHCP1, STCP, MR, OE)
diodes_green = SR(DS2, SHCP2, STCP, MR, OE)

diode_8_red = Pin(4, Pin.OUT)
diode_8_green = Pin(2, Pin.OUT)

game_loop = False
player_move = True
game_state = None

x_fields = [0, 0, 0, 0, 0, 0, 0, 0, 0]
o_fields = [0, 0, 0, 0, 0, 0, 0, 0, 0]

difficulty = difficulty_switch.value()

# Game logic based on the difficulty level
if difficulty:
    # Difficulty level is set to player mode
    board = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]

    light_diodes()

    while True:
        if player_move:
            for i, button in enumerate(control_buttons):
                if button.value() and board[i // 3][i % 3] == ' ':

                    game_loop = True
                    player_move = False
                    board[i // 3][i % 3] = 'X'

            light_diodes()
        else:
            if not is_board_full(board):

                x, y = calculate_best_move(board)

                board[x][y] = 'O'
                player_move = True
                
                light_diodes()

                if check_winner(board, 'O'):
                    game_state = 'O'
                    break
            else:
                break
else:
    # Difficulty level is set to computer mode
    # Chosing starting move for computer
     board = [[' ', ' ', ' '],
              [' ', ' ', ' '],
              [' ', ' ', ' ']]

    r = choice([1, 3, 5, 7])
    board[r // 3][r % 3] = 'O'

    light_diodes()

    while True:
        if player_move:
            for i, button in enumerate(control_buttons):
                if button.value() and board[i // 3][i % 3] == ' ':

                    game_loop = True
                    player_move = False
                    board[i // 3][i % 3] = 'X'

            light_diodes()
        else:
            if not is_board_full(board):
                x, y = calculate_best_move(board)
                
                board[x][y] = 'O'
                player_move = True
                
                light_diodes()

                if check_winner(board, 'O'):
                    game_state = 'O'
                    break
            else:
                break

# Flashing winning row
if game_state == 'O':
    coordinates = check_winning_coordinates(board)

    board[coordinates[0][0]][coordinates[0][1]] = '!'
    board[coordinates[1][0]][coordinates[1][1]] = '!'
    board[coordinates[2][0]][coordinates[2][1]] = '!'

    flash_led(coordinates)
