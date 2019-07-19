#! usr/bin/python3

# commandlineemail.py - Sends an email from your gmail address
# with the recipient and email content specified in the command
# line argument.

# USAGE: python3 commandlineemail.py <email recipient address>
# <email content string> - Logs into your email account and
# sends an email to <email recipient address> with the message
# being <email content string>.

import sys, time
from selenium import webdriver


def email_login_info():

    """Asks if the user would like to send the email from the
    default email address login stored in this program. If not,
    then ask them to enter the email name and password for
    an account which they would like to send from instead.
    """

    default_email_name = 'youremail@gmail.com'
    default_email_password = 'yourpassword'

    valid = {"yes": True, "ye": True, "y": True, "no": False, "n": False}

    change_account = input('Use %s to send email? (Yes/No) ' % default_email_name)

    # the prompt to change email account information must be
    # either yes or no. Re-prompt user until the response is valid
    while change_account.lower() not in valid:
        print('Must enter a valid response (Yes/No).')
        change_account = input('Use %s to send email? (Yes/No) ' % default_email_name)

    if not valid[change_account.lower()]:

        while True:
            email_name = input('Please enter a new gmail account name: ')
            if email_name.endswith('@gmail.com'):
                break
            else:
                print('The email account name %s is not a proper gmail account name' % email_name)

        email_password = input('Please enter the gmail account password: ')

    else:
        email_name = default_email_name
        email_password = default_email_password

    return email_name, email_password


def email_login(email_name, email_password):

    """Login to the specified email account sender. If the login
    fails, then declare the login has failed. Return a status
    of whether the login is successful as well as the webdriver
    object if successful.
    """

    # open up the gmail login page using the Firefox browser
    gmail_browser = webdriver.Firefox()
    gmail_browser.get('http://gmail.com')
    # find, clear, and fill in the email and password forms
    try:
        print('Logging into gmail...')
        # fill in the login username portion
        id_elem = gmail_browser.find_element_by_id('identifierId')
        id_elem.clear()
        id_elem.send_keys(email_name)
        time.sleep(3)

        # click the next button
        next_elem1 = gmail_browser.find_element_by_class_name('RveJvd')
        next_elem1.click()
        time.sleep(5)

        # fill in the password portion
        password_elem = gmail_browser.find_element_by_class_name('whsOnd')
        password_elem.clear()
        password_elem.send_keys(email_password)

        # click the next button
        next_elem2 = gmail_browser.find_element_by_class_name('RveJvd')
        next_elem2.click()

        print('Successful login into %s.' % email_name)
        login_complete = True
        return login_complete, gmail_browser

    except Exception as err:
        print('An error has occurred: %s' % err)
        print('The gmail login forms have changed. This '
              'program is not valid with the current forms.'
              ' Exiting now.')
        sys.exit()


def compose_email(gmail_browser, email_recipient, email_message):

    """For a given gmail browser object that has successfully
    logged in, click Compose button. Fill in the email recipient,
    email body message from the command line arguments. The
    email subject is filled in as: "Automated Email." Click
    the send button and close the browser.
    """
    try:
        # Find and click on compose button
        time.sleep(5)
        compose_elem = gmail_browser.find_element_by_class_name('T-I')
        compose_elem.location_once_scrolled_into_view
        compose_elem.click()

        # find and fill in the email recipient address
        time.sleep(5)
        recipient_elem = gmail_browser.find_element_by_class_name('vO')
        recipient_elem.clear()
        recipient_elem.send_keys(email_recipient)

        # find and fill in the subject line
        time.sleep(5)
        subject_elem = gmail_browser.find_element_by_class_name('aoT')
        subject_elem.clear()
        subject_elem.send_keys('Automated Email')

        # find and fill in the email body message
        time.sleep(5)
        body_elem = gmail_browser.find_element_by_class_name('Am')
        body_elem.clear()
        body_elem.send_keys(email_message)

        # find and click Send button
        send_elem = gmail_browser.find_element_by_class_name('T-I')
        send_elem.click()
        print('Email has been successfully sent to %s' % email_recipient)

        # close the webdriver object browser
        print('Closing the browser...')
        gmail_browser.quit()
        sys.exit()

    except Exception as err:
        print('An error has occurred: %s' % err)
        print('The gmail compose form has changed. This '
              'program is not valid with the current form.'
              ' Exiting now.')
        sys.exit()


if __name__ == "__main__":

    # extract the recipient address and email message from command
    # line arguments
    email_recipient = sys.argv[1]
    email_message = ' '.join(sys.argv[2:])

    # Attempt to gain the username and password info for the gmail
    # sender and then login to gmail. Prompt the user to try another
    # name and password combination if login does not succeed.

    login_attempt = False

    while not login_attempt:
        account_name, account_password = email_login_info()
        login_attempt, email_browser = email_login(account_name, account_password)
        time.sleep(5)

    # Attempt to compose the email and send it to the specified
    # recipient with the specified body message.
    compose_email(email_browser, email_recipient, email_message)