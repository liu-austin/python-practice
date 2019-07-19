#! /usr/bin/python3
# randomquizgenerator.py - Creates quizzes with questions and
# answers in random order, along with the answer key.

import random

# quiz data for the U.S. states and their corresponding capitals
# in a key-value dictionary

capitals = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix',
   'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver',
   'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee',
   'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois':
   'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas':
   'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine':
   'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston', 'Michigan':
   'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson', 'Missouri':
   'Jefferson City', 'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada':
   'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton',
   'New Mexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh',
   'North Dakota': 'Bismarck', 'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City',
   'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence',
   'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee':
   'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont':
   'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia':
   'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}

# generate 35 different quiz files
for quiznumber in range(35):
    # Create the zuie and answer key files
    quizfile = open('statecapitalquiz%s.txt' % (quiznumber+1), 'w')
    answerkeyfile = open('statecapitalquiz_answers%s.txt' % (quiznumber+1), 'w')

    # Write out the header for the quiz files
    quizfile.write('Name:\n\nDate:\n\nPeriod:\n\n')
    quizfile.write((' ' * 20) + 'State Capitals Quiz (Form %s)' % (quiznumber + 1))
    quizfile.write('\n\n')

    # Shuffle the order of the states.
    states = list(capitals.keys())
    random.shuffle(states)

    # Loop through the 50 randomized states and generate a question
    # for each one

    for index in range(len(states)):
        quizfile.write('Question %d: What is the capital city of %s?\n' % (index+1, states[index]))
        quiz





