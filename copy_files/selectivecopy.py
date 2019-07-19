#! /usr/bin/python3
# selectivecopy.py - A program that walks through a folder and
# searches for files with a certain file extension (such as .pdf
# or .jpg). These files are copied from whatever location they
# are in to a new folder.

# USAGE: python3 selectivecopy.py <folder location> - For a given
# folder location, the user is prompted to input a file extension
# type. The program walks through the folder location and copies
# all files with the inputted file extension type. They are
# pasted in a new folder called folder location_*file extension*.
# This new folder is located within the folder location.

import os, re, shutil, sys


def get_folder_location(location):

    """This function will check if the argument <folder location>
    is valid. If so, it returns the absolute folder location and
    it cannot be found, the program exits and prints that it
    could not find the folder location.
    """

    if os.path.exists(location):
        print('The folder location: ' + location + ' is valid.\nReady to walk through the folder location...\n')
        os.chdir(location)
        return os.path.abspath(location)
    else:
        sys.exit('The folder location: ' + location + ' could not be found.\n')


def get_file_extension():

    """This function takes in user-defined file extensions and
    checks if it is a proper file extension format.
    """

    while True:
        file_extension = input('Enter a file extension (.jpg, .txt, etc) to search for: \n')

        if file_extension.startswith('.'):
            break
        else:
            print('A valid file extension must begin with \'.\'.')

    print('Beginning to search the folder location for the file extension ' + file_extension + '.')
    return file_extension.lower()


# get the absolute folder path specified in the command line argument
folder_location = sys.argv[1]
abs_folder_location = get_folder_location(folder_location)

# ask user to input file extension and form regular expression
# based on it to search for files to copy in the folder path
file_extension = get_file_extension()
ends_with_string = '(' + file_extension + ')' + '$'
ext_regex = re.compile(ends_with_string)

# using os.walk(), search through the sub-folders of the main
# folder path for files that end with the user-inputted file
# extension. These found files are copied to a new folder
# located within the main folder path
print('Searching the sub-folders of ' + abs_folder_location + ' for files that end with: ' + file_extension)
copy_list = []
for foldername, subfolders, filenames in os.walk(abs_folder_location):
    os.chdir(foldername)

    for file in filenames:

        if ext_regex.search(file):
            copy_list.append(os.path.abspath(file))

if copy_list:
    new_folder_path = abs_folder_location + '_(' + file_extension[1:] + ')_copy'

    if not os.path.exists(new_folder_path):
        os.mkdir(new_folder_path)

    for file_to_copy in copy_list:
        shutil.copy(file_to_copy, new_folder_path)
    print('The files with the file extension ' + file_extension + ' located in the \nsub-folders of ' + abs_folder_location + ' are\n copied to: ' + new_folder_path)
else:
    print('No files with the file extension ' + file_extension + 'are located in the \nsub-folders of ' + abs_folder_location + '.')