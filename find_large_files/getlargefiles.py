#! /usr/bin/python3
# getlargefiles.py - A program that walks through a specified
# folder tree and searches for large files with file sizes
# of 100 MB or greater. The absolute paths of these files and
# folders are printed to the console.

# USAGE: python3 getlargefiles.py <folder path> - For a specified
# folder path, traverses the folder tree using os.walk() to
# search for files with sizes larger than 100 MB.
# The results are printed to the console.

import os, sys


def get_folder_location(location):

    """This function will check if the argument <folder location>
    is valid. If so, it returns the absolute folder location and
    it cannot be found, the program exits and prints that it
    could not find the folder location.
    """

    if os.path.exists(location):
        print('')
        print('The folder location: ' + location + ' is valid.\nReady to walk through the folder location...\n')
        os.chdir(location)
        return os.getcwd()
    else:
        print('')
        sys.exit('The folder location: ' + location + ' could not be found.\n')


def get_file_locations(location):

    """This function traverses the folder tree for the specified
    folder path. A list of all files in the sub-folders is
    gathered."""

    listoffiles = []

    for foldername, subfolders, filenames in os.walk(location):

        for file in filenames:
            listoffiles.append(os.path.join(foldername, file))

    if listoffiles:
        return listoffiles
    else:
        sys.exit('There are no files located within ' + location + '.')


def large_file_sizes(filelist):

    """This function searches through a list of files and prints
    a list of those files that have file sizes greater than or
    equal to 100 MB.
    """

    large_file_list = []

    for file in filelist:

        if os.path.getsize(file) >= 100000000:
            large_file_list.append(file)

    if large_file_list:
        print('FILE SIZES > 100 MB'.center(200, '-'))
        print(''.center(200, '-'))
        for file in large_file_list:
            print(file.ljust(176, ' ') + ('SIZE IN BYTES: ' + str(os.path.getsize(file))).rjust(20, ' '))
    else:
        print('FILE SIZES > 100 MB'.center(200, '-'))
        print(''.center(200, '-'))
        print('THERE ARE NO FILES IN THE FOLDER TREE WITH SIZES LARGER THAN 100 MB'.center(200, '-'))

    print('\n')
    return large_file_list


# extract the folder path from the system argument and return
# the absolute folder path
folder_location = sys.argv[1]
abs_folder_location = get_folder_location(folder_location)

# get the absolute file paths for all files in the folder tree
file_paths = get_file_locations(abs_folder_location)

# print the files with sizes greater than or equal to 100 MB
# along with their sizes
large_file_sizes(file_paths)