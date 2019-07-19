#! /usr/bin/python3
# phoneandemail.py - Copy a section of text to the clipboard and
# run phoneandemail.py. This script takes the copied text and
# searches through it for all phone numbers and email addresses
# , returning the matched results as a string to the clipboard.

import re, pyperclip

phoneregex = re.compile(r'''(
    (\d{3}|\(\d{3}\))?              # area code optional
    (\s|-|\.)?                      # separator
    (\d{3})                         # first 3 digits
    (\s|\.|-)                       # separator
    (\d{4})                         # last 4 digits
    (\s*(ext|ext.|x)\s*(\d{2.5}))?  # extension number      
    )''', re.VERBOSE)

emailregex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+               # email username
    (@)                             # points to email domain
    [a-zA-Z0-9.-]+                  # email domain name
    (\.)                            # dot
    [a-zA-Z]{2-4}                   # email domain ending
    )''', re.VERBOSE)

text = pyperclip.paste()

findphone = phoneregex.findall(text)
findemail = emailregex.findall(text)
matches = []

for groups in findphone:
    phonenum = '-'.join([groups[1], groups[3], groups[5]])
    if groups[8]!= '':
        phonenum+= ' x'+groups[8]
    matches.append(phonenum)
for groups in findemail:
    matches.append(groups[0])

if len(matches) > 0:
    pyperclip.copy('\n'.join(matches))
    print('Copied to clipboard:')
    print('\n'.join(matches))
else:
    print('No phone numbers or email addresses found.')
