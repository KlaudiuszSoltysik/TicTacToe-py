from machine import Pin
import time

from SR import SR


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
x_fields = [0, 0, 0, 0, 0, 0, 0, 0, 0]
o_fields = [0, 0, 0, 0, 0, 0, 0, 0, 0]

# MAIN LOOP
while True:
    if player_move:
        for i, button in enumerate(control_buttons):
            if button.value() and not x_fields[i]:
                game_loop = True
                # player_move = False
                x_fields[i] = 1

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
        # IMPOSSIBLE DIFFICULTY
        if difficulty_switch:
            pass
        # HARD DIFFICULTY
        else:
            pass

    time.sleep(0.2)
