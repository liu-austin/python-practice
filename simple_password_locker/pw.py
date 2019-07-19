#! /usr/bin/python3

# pw.py - An insecure password locker program.

PASSWORDS = {'email': 'fdsfsdsdffds',
             'blog': 'dfssdfsdfsdf',
             'luggage': 'fdsdfssdf'}

import sys, pyperclip
if len(sys.argv) < 2:
    print('Usage: python3 pw.py [account] -- copy account password')
    sys.exit()

account = sys.argv[1] #first command line arguement is the account name for password

if account in PASSWORDS:
    pyperclip.copy(PASSWORDS[account])
    print('Password for ' + account + ' copied to clipboard')
else:
    print('There is no account named ' + account)
