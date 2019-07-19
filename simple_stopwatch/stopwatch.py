#! usr/bin/python3
# stopwatch.py - A simple stopwatch program.


import pyperclip, time


# Display the program's instructions.
print('Press ENTER to begin. Afterwards, press ENTER to "click" the stopwatch. '
      'Press Ctrl-C to quit.')
input()                    # press Enter to begin
print('Started.')
startTime = time.time()   # get the first lap's start time
lastTime = startTime
lapNum = 1

try:
    while True:
        input()
        lapTime = round(time.time() - lastTime, 2)
        totalTime = round(time.time() - startTime, 2)
        textDisplay = 'Lap #' + str(lapNum).rjust(2) + ':' + str(totalTime).rjust(6) + ' (' + str(lapTime).rjust(6) + ')'
        pyperclip.copy(textDisplay)
        print(textDisplay)
        lapNum += 1
        lastTime = time.time() # reset the last lap time
except KeyboardInterrupt:
    # Handle the CTRL + C exception to keep its error message from displaying
    print('\nDone.')
