from machine import Pin
import time
import math

from SR import SR


def check_win():
    if any(field is None for field in board):
        return None
    elif board[0] == 'x' and board[1] == 'x' and board[2] == 'x' or board[3] == 'x' and board[4] == 'x' and board[5] == 'x' or board[6] == 'x' and board[7] == 'x' and board[8] == 'x' or board[0] == 'x' and board[3] == 'x' and board[6] == 'x' or board[1] == 'x' and board[4] == 'x' and board[7] == 'x' or board[2] == 'x' and board[5] == 'x' and board[8] == 'x' or board[0] == 'x' and board[4] == 'x' and board[8] == 'x' or board[2] == 'x' and board[4] == 'x' and board[6] == 'x':
        return -10
    elif board[0] == 'o' and board[1] == 'o' and board[2] == 'o' or board[3] == 'o' and board[4] == 'o' and board[5] == 'o' or board[6] == 'o' and board[7] == 'o' and board[8] == 'o' or board[0] == 'o' and board[3] == 'o' and board[6] == 'o' or board[1] == 'o' and board[4] == 'o' and board[7] == 'o' or board[2] == 'o' and board[5] == 'o' and board[8] == 'o' or board[0] == 'o' and board[4] == 'o' and board[8] == 'o' or board[2] == 'o' and board[4] == 'o' and board[6] == 'o':
        return 10
    else:
        return 0


def minimax(board, is_maxing):
    result = check_win()

    if result is not None:
        return result
    
    if is_maxing:
        best_score = -math.inf

        for i in range(len(board)):
            if board[i] is None:
                board[i] = 'o'
                score = minimax(board, False)
                board[i] = None

                if score > best_score:
                    best_score = score

    else:
        best_score = math.inf

        for i in range(len(board)):
            if board[i] is None:
                board[i] = 'x'
                score = minimax(board, True)
                board[i] = None

                if score < best_score:
                    best_score = score
    
    return best_score


def light_diodes():
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


# DEFINE PINS
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

player_move = True
game_loop = False
board = [None, None, None, None, None, None, None, None, None]
x_fields = [0, 0, 0, 0, 0, 0, 0, 0, 0]
o_fields = [0, 0, 0, 0, 0, 0, 0, 0, 0]

# MAIN LOOP
while True:
    if player_move:
        for i, button in enumerate(control_buttons):
            if button.value() and not x_fields[i] and not o_fields[i]:
                game_loop = True
                player_move = False
                x_fields[i] = 1
                board[i] = 'x'

                light_diodes()
    else:
        # IMPOSSIBLE DIFFICULTY
        if difficulty_switch:

            best_score = -math.inf
            best_move = None

            for i in range(len(board)):
                if board[i] is None:
                    board[i] = 'o'
                    score = minimax(board, False)
                    board[i] = None

                    if score > best_score:
                        best_score = score
                        best_move = i

            o_fields[best_move] = 1
            board[best_move] = 'o'
            player_move = True

            light_diodes()

        # HARD DIFFICULTY
        else:
            pass

    time.sleep(0.1)
