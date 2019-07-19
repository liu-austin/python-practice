#! /usr/bin/python3

# madlibs.py - A program that reads Mad Libs text files and
# prompts users to input adjectives, nouns, adverbs, and verbs
# to complete the Mad Libs text. A new file with the inputted
# words to complete the Mad Libs expressions is outputted.

# USAGE: python3 madlibs.py <text file> - reads the text file and
# prompts the user to complete the Mad Libs expressions. The
# program takes the user inputs and replaces the Mad Libs fields
# and returns the completed Mad Libs expressions in a new file
# called <new_text file>.

import re, sys

expression_finder_regex = re.compile(r'ADJECTIVE|NOUN|VERB|ADVERB')

if sys.argv[1].endswith('.txt'):
    text_file = sys.argv[1]
else:
    sys.exit('The argument ' + sys.argv[1] + ' is not a .txt file.\n'
            'Please view the following usage notes:\n\n'
            'USAGE: python3 madlibs.py <text file> - reads the text file and '
            'prompts the user to complete the Mad Libs expressions. The '
            'program takes the user inputs and replaces the Mad Libs fields '
            'and returns the completed Mad Libs expressions in a new file '
            'called <new_text file>.\n')

madlibs_prompt = open(sys.argv[1], 'r')

new_file = 'new_'+sys.argv[1]
madlibs_completed = open(new_file, 'w')

read_prompt = madlibs_prompt.read()

fill_in = []

find_entries = expression_finder_regex.findall(read_prompt)

for entry in find_entries:
    fill_in.append(input('Enter an ' + entry.lower() + ':\n'))

filled_prompt = (expression_finder_regex.sub('%s', read_prompt) % tuple(fill_in))
madlibs_completed.write(filled_prompt)

madlibs_prompt.close()
madlibs_completed.close()

print('The completed Mad Lib is outputted to the file: ' + new_file + ' and below:\n')
print(filled_prompt+'\n')
