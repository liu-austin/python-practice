#this function takes in a list that contains sublists as list values
#the list appears as an image and the function rearranges the sublist
#values and returns a new list that appears as a rotated image of the
#original list image

def char_pic_grid(*args):
    '''the function char_pic_grid takes in a list as an input
    and returns a list with the sublists in a new order
    '''

    for i in range(len(args[0])):
        for j in range(len(args)):
            print(args[j][i], end='')
        print('')
