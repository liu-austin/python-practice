#! usr/bin/python3

#printTable.py - printTable() function takes in a list of
#sub-lists that are equal lengths. It returns the sub-lists
#as formatted rows that are right-adjusted.

#while True:
 #   listoflists = input('Input a list that contains '
  #                      'sub-lists of equal length:\n')
   # if isinstance(listoflists, list):
    #    break
   # else:
    #    print('Input must be a list.')

listoflists = [['apples', 'oranges', 'cherries', 'banana'],
             ['Alice', 'Bob', 'Carol', 'David'],
             ['dogs', 'cats', 'moose', 'goose']]

adjustlength= 0 #maximum characters in a sub-list used to
#determine the amount to adjust by
tablerows = [] #list that contains the rows of the returned
#table

for i in range(len(listoflists[0])):
    storage='' #storage variable
    for j in range(len(listoflists)):
        storage+= ' '+listoflists[j][i]
    tablerows.append(storage)

    if len(tablerows[i])> adjustlength:
        adjustlength = len(tablerows[i])

for i in range(len(tablerows)):
    print(tablerows[i].rjust(adjustlength))

