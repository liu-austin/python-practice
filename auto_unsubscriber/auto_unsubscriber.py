#! usr/bin/python3
# auto_unsubscriber.py - This script searches your
# emails for unsubscribe links and opens those links.

# USAGE: python3 auto_unsubscriber.py <password> - <password>
# is the email login password to access the IMAP server.

import bs4, imapclient, imaplib, pyzmail, sys, webbrowser


email_account_name = 'example_account@gmail.com'


def email_login(login_name):

    """This function attempts to login to the IMAP
    server for the scripted login name. The user is
    prompted for a password until a successful login
    occurs."""

    # Contact the IMAP client for the user email
    imap_object = imapclient.IMAPClient('imap.gmail.com', ssl=True)
    valid_login = False
    # If password provided in command line argument,
    # attempt to login.
    if len(sys.argv) > 1:
        try:
            email_account_password = sys.argv[1:]
            imap_object.login(login_name, email_account_password)
            valid_login = True
            print('Successful login to %s' % email_account_name)
        except Exception as error:
            print('The login attempt is unsuccessful.\nAn error has occurred: %s' % error)

        # Attempt to login using the user-inputted passwords
        # until a successful login attempt.
        while not valid_login:
            try:
                email_account_password = input('Enter the password: ')
                imap_object.login(login_name, email_account_password)
                valid_login = True
                print('Successful login to %s' % email_account_name)
            except Exception as error:
                print('The login attempt is unsuccessful.\nAn error has occurred: %s' % error)

    return imap_object


def walk_folders(imap_obj):

    """This function creates a UID for every email
    in every folder for the email account."""

    # Go through the list_folders method and append
    # the folder names to the folder name dictionary.
    folder_uids = {}
    imaplib._MAXLINE = 10000000
    for email_folder in imap_obj.list_folders():
        imap_obj.select_folder(email_folder[len(email_folder) - 1], readonly=True)
        folder_uids[email_folder[email_folder[len(email_folder) - 1]]] = imap_obj.search(['ALL'])

    return imap_obj, folder_uids


def find_unsubscribe_links(imap_obj, **folder_uids):

    """This function searches through the UID list
     for unsubscribe links and opens them."""

    # For each folder, search through each UID's html
    # part and find unsubscribe links to open. Open
    # those links.
    for folder in folder_uids:
        for uid in folder:
            raw_message = imap_obj.fetch([uid], ['BODY[]'])
            message = pyzmail.PyzMessage.factory(raw_message[uid]['BODY[]'])
            if message.html_part:
                message_html_part = message.html_part.get_payload().decode(message.html_part.charset)
                bs4_obj = bs4.BeautifulSoup(message_html_part, "html5lib")
                unsub_elements = bs4_obj.select('a[class="unsubscribe"]')
                    if not unsub_elements:
                        unsub_link = unsub_elements[0].get('href')
                        webbrowser.open(unsub_link)
                        print('Unsubscribe link opened at: %s' % unsub_link)


if __name__ == "__main__":
    find_unsubscribe_links(walk_folders(email_login(email_account_name)))
