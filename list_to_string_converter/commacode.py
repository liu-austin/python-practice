#function that takes in a list of any length as input and returns
#a string that contains all of the list values in order, separated
#by a ',' and an 'and.' The last list value is separated by an
#additional 'and' from the second-to-last list value.

def commacode(*args):
    '''This function takes in a list of any size and returns a string\
     that contains all of the list values, separated by a comma and a\
     space. An additional 'and' separates the second-to-last and last\
     list values.\
     '''

    commacodestring = ''
    for i in range(len(args)):
        commacodestring+=str(args[i])
        if i ==len(args)-1:
            break
        commacodestring+=','
        if i==len(args)-2:
            commacodestring+=' and '
        else:
            commacodestring+=' '

    return(commacodestring)

