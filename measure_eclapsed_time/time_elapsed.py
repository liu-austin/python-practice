#! usr/bin/python3
# time_elapsed.py - This script measures the amount of
# time until or has passed from some point in the past
# or future.


import datetime, sys


# Prompt the user to enter the year, month, day, hour,
# minute, second, microseconds for the date of interest.
print('Enter the values for the date of interest as integers below:')
year = int(input('Enter the year of the date of interest: '))
month = int(input('Enter the month of the date of interest: '))
day = int(input('Enter the day of the date of interest: '))
hour = int(input('Enter the hour of the date of interest: '))
minute = int(input('Enter the minute of the date of interest: '))
second = int(input('Enter the second of the date of interest" '))

# Convert the inputted string values into a Datetime object.
try:
    dateofinterest = datetime.datetime(year, month, day, hour, minute, second)

except ValueError as exception:
    print('An error has occurred: %s.' % exception)
    print('The time value inputted is not valid.')
    sys.exit('Exiting now.')

# Calculate the time difference between the date of interest
# and current time
presenttime = datetime.datetime.now()
timeelapsed = dateofinterest - presenttime
print('The time difference between the date of interest and the current time is: ')
print(str(timeelapsed))
