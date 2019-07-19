#! usr/bin/python3

# play2048.py - Opens and plays the 2048 game on Firefox browser
#
# USAGE: python3 play2048.py - This script uses a Selenium
# Firefox browser that opens the 2048 game url. It starts the
# game and applies a loop of up, right, down, left inputs
# until the game is over. The user can decide whether to
# quit or replay the game.


import sys, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Open the 2048 game in a Firefox browser
game_url = 'https://gabrielecirulli.github.io/2048/'
browser = webdriver.Firefox()
restart_game = 'y';

while restart_game != 'n':
    try:
        browser.get(game_url)

        # Click the 'New Game' button
        start_elem = browser.find_element_by_class_name('restart-button')
        start_elem.click()

    except Exception as err:
        print('An error has occurred while accessing the game: %s' % err)
        sys.exit('Exiting from the script.')

    # Send up, right, down, left key commands to the game
    try:
        html_elem = browser.find_element_by_tag_name('html')

        while True:
            html_elem.send_keys(Keys.UP)
            # time.sleep(0.5)
            html_elem.send_keys(Keys.RIGHT)
            # time.sleep(0.5)
            html_elem.send_keys(Keys.DOWN)
            # time.sleep(0.5)
            html_elem.send_keys(Keys.LEFT)
            # time.sleep(0.5)
            try:
                game_over_elem = browser.find_element_by_class_name('game-over')
                game_over = True
            except:
                game_over = False

            if game_over:
                break

    except Exception as err:
        print('An error has occurred while playing the game: %s' % err)
        sys.exit('Exiting from the script.')

    # Prompt user to restart or quit the game
    user_input = ''
    valid_response = ['y', 'n']
    while user_input.lower() not in valid_response:
        user_input = input('Would you like to restart the game? (y/n): ')

    restart_game = user_input
    if restart_game == 'n':
        browser.quit()