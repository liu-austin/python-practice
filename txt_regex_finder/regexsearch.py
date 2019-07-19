#! /usr/bin/python3
# regexsearch.py - A program that searches all .txt files in a
# chosen folder for any line that matches a user-supplied
# regular expression. The results are printed to the screen.

# USAGE: python3 regexsearch.py <folder path> - Searches all .txt
# files in the specified folder for a user-given regular
# expression. Outputs the results to the console.

import re, sys, os

folder_path = sys.argv[1]

# determine if the specified folder path is an actual directory
if os.path.isdir(folder_path):
    print('The directory', folder_path, 'is valid.\n')
else:
    sys.exit('The directory ' + folder_path + ' could not be found.\n')

# get the name of the folder path
if os.path.isabs(folder_path):
    abs_folder_path = folder_path
else:
    abs_folder_path = os.path.abspath(folder_path)

file_names = os.listdir(abs_folder_path)
txt_file_names = []

# create a absolute file path name for valid .txt files in the path
for file_index in file_names:
    if file_index.endswith('.txt'):
        txt_file_names.append(os.path.join(abs_folder_path, file_index))

# allow the user to input a regular expression to search the .txt files for and output the
# found results on the console
user_regex = re.compile(input(r'Enter a regular expression to search the .txt files: '))

# search the .txt files for the user-defined regular expression
# and print the lines that contain them
for txt_file in txt_file_names:
    print('\n' + 'Results for ' + txt_file + ':')
    with open(txt_file) as file_handle:
        for line in file_handle.readlines():
            if user_regex.findall(line):
                print(line)