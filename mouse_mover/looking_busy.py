#! usr/bin/python3
# looking_busy.py - This script runs in the background and
# slightly moves the mouse cursor to the side every ten
# seconds to prevent the computer reaching an idle status.
# The command 'CTRL + C' can be evoked to stop this program.


import pyautogui, sys, time


pyautogui.FAILSAFE = True

screen_width, screen_height = pyautogui.size()
frequency = 10  # seconds before cursor adjustment

try:
    while True:
        time.sleep(frequency)
        x_pos, y_pos = pyautogui.position()
        # Determine which direction to shift the cursor from
        # current cursor position on screen
        # If cursor position is to the right
        if x_pos >= int(screen_width/2):
            x_adjust = -1  # shift cursor to left
        else:
            x_adjust = 1  # shift cursor to right
        if y_pos >= int(screen_height/2):
            y_adjust = -1  # shift cursor up
        else:
            y_adjust = 1  # shift cursor down
        # move the cursor slightly instantaneously
        pyautogui.moveRel(x_adjust, y_adjust)
except KeyboardInterrupt:
    sys.exit('CTRL + C Input Detected.\nExiting now.')
