#! usr/bin/python3
# photo_folder_finder.py - This script searches through every
# folder on the hard drive and prints the absolute paths of
# folders that contain at least 50% files that are .jpg or .png.
# In addition, the images must have heights and widths greater than
# 500 pixels.


import os
from PIL import Image


for foldername, subfolders, filenames in os.walk(os.getenv('HOME')):
    numPhotoFiles = 0
    numNonPhotoFiles = 0
    for filename in filenames:
        # Check if file extension isn't .png or .jpg.
        if not (filename.lower().endswith('.jpg') or filename.lower().endswith('.png')):
            numNonPhotoFiles += 1
            continue    # skip to next filename

        # Open image file using Pillow.
        image_file = Image.open(os.path.join(foldername, filename))
        # Check if width & height are larger than 500.
        if image_file.size[0] >= 500 and image_file.size[1] >= 500:
            # Image is large enough to be considered a photo.
            numPhotoFiles += 1
        else:
            # Image is too small to be a photo.
            numNonPhotoFiles += 1

    # If more than half of files were photos,
    # print the absolute path of the folder.
    if numPhotoFiles >= numNonPhotoFiles:
        print('Folder folder location at: %s' % foldername)
