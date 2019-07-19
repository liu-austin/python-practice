#! usr/bin/python3
# keyboardinterrupt.py - Allows user to press CTRL + C
# to cancel an action.


import sys, time


def keyboardinterrupt():

    """Gives a 5 second delay using time.sleep()
    method. During delay, prompts user if they
    want to abort current action using the CTRL + C
    interrupt. If CTRL + C is pressed, catch the
    KeyboardInterrupt exception and exits the running
    process. Otherwise, the process proceeds normally.
    """

    sleep_duration = 5
    # Give 5 second pause to let user press CTRL+C
    try:
        print('To abort the current running process, press CTRL + C.\n'
              'Note: This will close this instance of Python and all other'
              'processes running on it.')
        for countdown in range(sleep_duration):
            print('%s seconds left before continuing process...' % (5 - sleep_duration))
            time.sleep(1)
    except KeyboardInterrupt as exception:
        print('%s detected.' % exception)
        print('Current process aborted.\n'
              'Exiting from Python.')
        sys.exit()
