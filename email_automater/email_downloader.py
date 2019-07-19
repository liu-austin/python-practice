#! usr/bin/python3
# email_downloader.py - This script checks an email account every 15 minutes and executes instructions
# from new emails sent to that account.

# USAGE: python3 email_downloader.py <password> - Logs in to the account with the corresponding <password>.
# Send an email to the <automation_email_address> containing email subject = <password>. The email sender
# must be the <specified_address> or else the orders in the email are not followed. The email body contains
# a dictionary for the link as follows:
# <link to file>
# The next line contains the name of the file:
# <file name>
# This script automatically opens the file using the default program selected unless another program is
# specified. This is given as a dictionary as follows:
# 'DEFAULT'
# to use the default program. Or:
# Program path to use instead>.
# The email is deleted afterwards and a text notification is sent to the user's cell number via Twilio.


import imapclient, imaplib, os, pyzmail, requests, shelve, subprocess, sys, threading
from twilio.rest import Client


class AccountInfo:

    """This class contains the account information for the email sender and recipient, Twilio SID and
     authentication, and sender and recipient phone numbers."""

    def __init__(self, password, sender_address, receiver_address,
                 receiver_password, twilio_sid, twilio_number,
                 twilio_token, phone_number):

        """This method contains the initialization variables for the communication account information."""

        self.password = password
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.receiver_password = receiver_password
        self.twilio_sid = twilio_sid
        self.twilio_number = twilio_number
        self.twilio_token = twilio_token
        self.phone_number = phone_number

    def save_account(self):

        """This method saves the account data to a shelve file."""

        shelf_file = shelve.open('account_data')
        account_info = [self.sender_address, self.receiver_address,
                        self.receiver_password, self.twilio_sid,
                        self.twilio_number, self.twilio_token,
                        self.phone_number]
        shelf_file[self.password] = account_info
        shelf_file.close()
        print('Account information has been updated.')


class ProcessEmail(AccountInfo):

    """This class logs into the receiver email address and looks
    at sent emails. Emails sent by the specified sender address have
    the commands specified in the body executed. Emails are deleted."""

    def email_login(self):

        """This method logs into the receiver email address."""

        imap_object = imapclient.IMAPClient('imap.gmail.com', ssl=True)
        imap_object.login(' ' + self.receiver_address + ' ', ' ' + self.receiver_password + ' ')
        print('Successful login to: %s' % self.receiver_address)
        return imap_object

    def search_and_execute(self, imap_object):

        """This method looks through inbox emails and sees if the sender
        is the specified sender address. If it is, it executes commands
        from the email body. All searched emails are then deleted."""

        download_folder = os.path.join(os.path.join(os.getenv('HOME'), 'Desktop'), 'Email Downloads')
        os.makedirs(download_folder, exist_ok=True)
        imap_object.select_folder('INBOX', readonly=False)
        imaplib._MAXLINE = 10000000
        UIDs = imap_object.search(['ALL'])
        # If no email search results are found, exit program.
        if not UIDs:
            sys.exit('No new emails were found in the inbox.\nExiting now.')
        # For a email found in the inbox, search the text portion.
        for UID in UIDs:
            raw_message = imap_object.fetch([UID], ['BODY[]'])
            message = pyzmail.PyzMessage.factory(raw_message[UID][b'BODY[]'])
            successful_download = False
            # Check if the sender address and password are correct.
            if (message.get_subject() == self.password) and (message.get_addresses('from')[0][1] == self.sender_address):
                if message.text_part:
                    text = message.text_part.get_payload().decode(message.text_part.charset)
                    commands = text.split(', ')[:3]
                    # Download the web link.
                    try:
                        file = requests.get(commands[0])
                        file.raise_for_status()
                        file_path = os.path.join(download_folder, commands[1])
                        with open(file_path, 'wb') as file_handler:
                            for chunk in file.iter_content(100000):
                                file_handler.write(chunk)
                        print('File at: %s has successfully been accessed.' % commands[0])
                    except Exception as error:
                        print('An error has occurred: %s' % error)
                        sys.exit('Quitting now.')
                    # Launch the file in a separate thread
                    threads = []
                    try:
                        if commands[2].upper() == 'DEFAULT':
                            thread_object = threading.Thread(target=subprocess.Popen, args=[['see', file_path]])
                        # Use the program path specified in the third line instead of default program
                        else:
                            thread_object = threading.Thread(target=subprocess.Popen, args=[[commands[2], file_path]])
                        threads.append(thread_object)
                        thread_object.start()
                        successful_download = True
                    except Exception as error:
                        print('An error has occurred: %s' % error)
                    print('The file has successfully been downloaded to: %s' % file_path)
                    if successful_download:
                        download_result = [True, commands[1]]
                    else:
                        download_result = [False, commands[1]]
                    # Call the function to send a Twilio text message.
                    send_text(self, download_result)
                    for thread in threads:
                        thread.join()
            print('The email with UID: %s has been deleted.' % UID)
            imap_object.delete_messages(UID)
        imap_object.logout()
        print('The email account has been logged out.')


def account_login():

    """This function logs in to an object of the AccountInfo class."""

    successful_login = False
    password = ''
    shelf_file = shelve.open('account_data')
    while not successful_login:
        if len(sys.argv) > 1 and not password:
            password = ' '.join(sys.argv[1:])
        else:
            password = input('Enter a password for an account: ')
        try:
            if len(shelf_file[password]) == 7:
                account_info = shelf_file[password]
                print('Successful login attempt.')
                successful_login = True
        except KeyError as error:
            print('Unsuccessful login attempt.\nAn error has occurred: %s' % error)
    shelf_file.close()
    logged_in = ProcessEmail(password, account_info[0], account_info[1], account_info[2],
                             account_info[3], account_info[4], account_info[5], account_info[6])
    return logged_in


def create_account():

    """This function prompts users to input account info to
    create an AccountInfo object."""

    print('Enter valid data below to create a new AccountInfo object.')
    password = input('Enter a password: ')
    sender_address = input('Enter the sender_address: ')
    receiver_address = input('Enter the receiver address (gmail account): ')
    receiver_password = input('Enter the receiver password: ')
    twilio_sid = input('Enter the Twilio SID: ')
    twilio_number = input('Enter the Twilio phone number: ')
    twilio_token = input('Enter the Twilio authentication token: ')
    phone_number = input('Enter the phone number to text to: ')
    user = ProcessEmail(password, sender_address, receiver_address, receiver_password,
                        twilio_sid, twilio_number, twilio_token, phone_number)
    user.save_account()
    print('Account information for password: %s has been created.' % password)


def send_text(processor, *download_info):

    """This function sends a text message via Twilio to inform the user that the file has
    been downloaded."""

    twilio_client = Client(processor.twilio_sid, processor.twilio_token)
    if download_info[0]:
        body_content = 'The file: ' + download_info[0][1] + ' is currently downloading.'
        message = twilio_client.messages.create(body=body_content, from_=processor.twilio_number, to=processor.phone_number)
    else:
        body_content = 'The file: ' + download_info[0][1] + ' has failed to download'
        message = twilio_client.messages.create(body=body_content, from_=processor.twilio_number, to=processor.phone_number)
    print(message.body)


if __name__ == "__main__":
    email_object = account_login()
    email_object.search_and_execute(email_object.email_login())
