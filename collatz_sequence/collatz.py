#script that calls a function that takes an integer input and returns the collatz function output of the input,
#and iteratively returns the collatz function output of the previously returned collatz output
#until the collatz function output returns 1.

def collatz(number):
    '''Function that simulates the Collatz sequence by taking an integer input and
    returns a value based on its value and if it is even or odd. When called iteratively,
    it uses the previous output as input until the final output value of 1.'''
    try:
        number = int(number) #change the input into an integer
        if (number%2)==0: # if number is even, return (number//2)
            return (number//2)
        if (number%2)==1: # if number is odd, return (3*number+1)
            return (number*3+1)
    except ZeroDivisionError:
        print("Cannot divide by zero!")

print("This script will call on the collatz function to simulate the\nCollatz sequence. Please enter any integer.")
number = input("Enter number:\n")
while True:
    try:
        number = collatz(number)
        print(number)
        if number ==1:
            break
    except ValueError:
        print(number +" is not a valid number input!")
        break