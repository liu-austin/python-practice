#! usr/bin/python3
# custom_seating_cards.py - This script creates a seating
# card for each guest name in th guest list.


import os
from PIL import Image, ImageDraw, ImageFont


# Each seating card has 4 x 5 inch dimensions.
card_height = 288  # pixels
card_width = 360  # pixels

# Fonts folder path
fonts_folder_path = '/usr/share/fonts/truetype'

# Open guest list file and get guest names.
guest_list_path = os.path.join(os.path.join(os.path.join(os.getenv('HOME'), 'Desktop'),
                                            os.path.join('pythonprograms', 'automate_online-materials')), 'guests.txt')

with open(guest_list_path) as guest_list:
    guest_names = guest_list.readlines()
    # Create seating card images for each guest
    for guest in guest_names:
        # Create a card background with black border
        card_image = Image.new('RGBA', (card_height, card_width), 'black')
        # Separate the black border from the main card image
        decorate = ImageDraw.Draw(card_image)
        decorate.rectangle((10, 10, 350, 278), fill='tan')
        # Draw circles around the border
        # Along left side
        for along_left_side in range(25, 285, 20):
            decorate.ellipse((25, along_left_side, 45, along_left_side+20), fill='red', outline='black')
        # Along top side
        for along_top_side in range(45, 335, 20):
            decorate.ellipse((along_top_side, 25, along_top_side+20, 45), fill='red', outline='black')
        # Along right side
        for along_right_side in range(25, 285, 20):
            decorate.ellipse((315, along_right_side, 335, along_right_side+20), fill='red', outline='black')
        # Along bottom side
        for along_bottom_side in range(45, 335, 20):
            decorate.ellipse((along_bottom_side, 245, along_bottom_side+20, 265), fill='red', outline='black')
        # Set the font
        arial_font = ImageFont.truetype(os.path.join(fonts_folder_path, 'arial.ttf'), 32)
        # Write the name for the seating
        decorate.text((card_height/2, card_width/2), guest, fill='black', font=arial_font)
        card_image.save('%s_card.png' % guest)
