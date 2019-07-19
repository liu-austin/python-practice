#! usr/bin/python3
# random_chore_emailer.py - Pairs random chores to a list of
# email addresses and sends emails to each address containing
# the assignments.


import random, smtplib


# Email account login info
email_account = 'senderperson@gmail.com'

# list of chores to choose from
list_of_chores = ['water plants',
                  'clean kitchen',
                  'vacuum',
                  'remove trash',
                  'mow lawn',
                  'clean bathroom',
                  'get supplies',
                  'sweep yard',
                  'schedule appointment',
                  'organize storage',
                  'prepare meals',
                  'get appliance fixed',
                  'move furniture',
                  'set up home automation',
                  'clean garage']
# list of email addresses to randomly assign chores to
list_of_email_addresses = ['person1@gmail.com',
                           'person2@gmail.com',
                           'person3@gmail.com',
                           'person4@gmail.com',
                           'person5@gmail.com',
                           'person6@gmail.com']


def chore_assigner(number_of_chores):

    """This function randomly assigns chores to each email
    address based on the function input. Each person cannot
    receive the same chore twice."""

    chore_assignments = {}
    # Go through each address and add chores randomly
    for address in list_of_email_addresses:
        chore_assignments[address] = []
        chores_selected = []
        # Assign a number of chores for everyone based on the
        # function input
        for current_chore_number in range(number_of_chores):
            redundant_task = True
            # Check to see if this email address has already been
            # assigned this chore already.
            while redundant_task:
                random_chore = random.choice(list_of_chores)
                # Select another random chore until one that has
                # not been assigned to this email is chosen
                if random_chore in chores_selected:
                    continue
                else:
                    chores_selected.append(random_chore)
                    chore_assignments[address].append()
                    redundant_task = False

    print('%s chores have been assigned to everyone.' % number_of_chores)
    return chore_assignments


def send_emails(**assigned_chore_list):

    """This function sends emails to all addresses on the mailing
    list. The email contents include the list of chores each
    email account owner has been assigned."""

    # Login to email account
    smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_object.ehlo()
    smtp_object.starttls()
    password = input('Enter the email sender account password: ')
    smtp_object.login(email_account, password)

    # for each email address that has chores assigned, send it
    # an email containing the chores the account owner has to
    # complete.
    for account in list_of_email_addresses:
        body = "Subject: Chores To Complete\nTo %s,\nHere are the" \
               "chores that have been assigned for you to complete:\n" \
               "%s" % (account[:len(account)-10], assigned_chore_list[account])
        print('Sending email to: %s' % account)
        send_mail_status = smtp_object.sendmail(email_account, account, body)
        if send_mail_status != {}:
            print('There was a problem sending email to %s: %s' % (account, send_mail_status))

    smtp_object.quit()


if __name__ == "__main__":
    # Prompt user to input a valid number of chores to select
    valid_number = False
    while not valid_number:
        try:
            amount_of_chores = int(input('How many chores to randomly assign to each email address: '))
        except Exception as error:
            print('An error has occurred: %s.\nThe input provided is invalid' % error)
            print('The input provided must be an integer between 1 and %s' % len(list_of_chores))
        if 0 < amount_of_chores <= len(list_of_chores):
            valid_number = True
        else:
            print('The input provided must be an integer between 1 and %s' % len(list_of_chores))

    send_emails(chore_assigner(amount_of_chores))
    print('Finished executing.')
