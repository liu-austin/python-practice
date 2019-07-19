#! /usr/bin/python3
# mcb.pyw - Multi-clipboard file that writes field entry data
# to a keyword, copies the field entry data for a keyword to the
# clipboard, or lists all of the keywords stored in the program.

# Usage: python3 mcb.pyw save <keyword> - Saves clipboard to keyword
# Usage: python3 mcb.pyw <keyword> - Loads field entry data for associated keyword to clipboard
# Usage: python3 mcb.pyw list - Loads all keywords to the clipboard
# Usage: python3 mcb.pyw delete <keyword> - Delete the keyword key-value
# Usage: python3 mcb.pyw delete - Delete every keyword key-value

import pyperclip, sys, shelve

mcbshelf = shelve.open('mcb')

if len(sys.argv) == 3:
    if sys.argv[1].lower() == 'save':
        mcbshelf[sys.argv[2]] = pyperclip.paste()
    elif sys.argv[1].lower() == 'delete':
        try:
            del mcbshelf[sys.argv[2]]
        except KeyError:
            pyperclip.copy('The keyword \'' + sys.argv[2] + '\' could not be found.')
    else:
        pyperclip.copy('The keyword or usage format does not match '
                       'any found in this program. Please review the '
                       'following usage format:\n'
                       'USAGE: python3 mcb.pyw save <keyword> - Saves clipboard to keyword\n'
                       'USAGE: python3 mcb.pyw <keyword> - Saves the field entry info for the keyboard to clipboard\n'
                       'USAGE: python3 mcb.pyw <list> - Saves all stored keywords to clipboard\n'
                       'USAGE: python3 mcb.pyw delete <keyword> - Deletes the field entry info for the keyword\n'
                       'USAGE: python3 mcb.pyw delete - Deletes every stored field entry info\n')

elif len(sys.argv) == 2:
    if sys.argv[1].lower() == 'list':
        pyperclip.copy(str(list(mcbshelf.keys())))
    elif sys.argv[1].lower() in list(mcbshelf.keys()):
        pyperclip.copy(mcbshelf[sys.argv[1]])
    elif sys.argv[1].lower() == 'delete':
        mcbshelf = {}
    else:
        pyperclip.copy('The keyword or usage format does not match '
                       'any found in this program. Please review the '
                       'following usage format:\n'
                       'USAGE: python3 mcb.pyw save <keyword> - Saves clipboard to keyword\n'
                       'USAGE: python3 mcb.pyw <keyword> - Saves the field entry info for the keyboard to clipboard\n'
                       'USAGE: python3 mcb.pyw <list> - Saves all stored keywords to clipboard\n'
                       'USAGE: python3 mcb.pyw delete <keyword> - Deletes the field entry info for the keyword\n'
                       'USAGE: python3 mcb.pyw delete - Deletes every stored field entry info\n')

else:
    pyperclip.copy('The keyword or usage format does not match '
                   'any found in this program. Please review the '
                   'following usage format:\n'
                   'USAGE: python3 mcb.pyw save <keyword> - Saves clipboard to keyword\n'
                   'USAGE: python3 mcb.pyw <keyword> - Saves the field entry info for the keyboard to clipboard\n'
                   'USAGE: python3 mcb.pyw <list> - Saves all stored keywords to clipboard\n'
                   'USAGE: python3 mcb.pyw delete <keyword> - Deletes the field entry info for the keyword\n'
                   'USAGE: python3 mcb.pyw delete - Deletes every stored field entry info\n')

mcbshelf.close()