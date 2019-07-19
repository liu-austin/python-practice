#! usr/bin/python3
# resizeAndAddLogo.py - Resizes all images in current working directory to fit
# in a 300x300 square, and adds catlogo.png to the lower-right corner.


import os
from PIL import Image


SQUARE_FIT_SIZE = 300
LOGO_FILENAME = 'catlogo.png'
logoIm = Image.open(LOGO_FILENAME)
logoWidth, logoHeight = logoIm.size

os.makedirs('withLogo', exist_ok=True)
# Loop over all files in the working directory.
for filename in os.listdir('.'):
    if not (filename.lower().endswith('.png') or filename.lower().endswith('.jpg') or filename.lower().endswith('.gif')
            or filename.lower().endswith('.bmp')) or filename == LOGO_FILENAME:
        continue  # skip non-image files and the logo file itself
    im = Image.open(filename)
    width, height = im.size

    # Check if image needs to be resized.
    if width > SQUARE_FIT_SIZE and height > SQUARE_FIT_SIZE:
        # Calculate the new width and height to resize to.
        if width > height:
            height = int((SQUARE_FIT_SIZE / width) * height)
            width = SQUARE_FIT_SIZE
        else:
            width = int((SQUARE_FIT_SIZE / height) * width)
            height = SQUARE_FIT_SIZE

    # Check if the height or width of the image is at least twice
    # the height and width of the logo image before adding the logo.
    # Otherwise, skip adding the logo.
    if (height <= 2*logoHeight) or (width <= 2*logoWidth):
        print('The image dimensions are too small for pasting the logo. Skipping.')

    # Resize the image.
    print('Resizing %s...' % (filename))
    im = im.resize((width, height))
    # Add the logo.
    print('Adding logo to %s...' % (filename))
    im.paste(logoIm, (width - logoWidth, height - logoHeight), logoIm)

    # Save changes.
    im.save(os.path.join('withLogo', filename))
