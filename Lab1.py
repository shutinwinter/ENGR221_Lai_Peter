# Peter Lai
# Lab1.py
# Lab 1
# 27 January 2025

message = "Go gators!"
# Declare's variable 'message' containing string 'Go Gators!'

print(message)
# Prints statement to print value 'message' to terminal


import random          # imports the library named random

def rps():
    """This plays a game of rock-paper-scissors
       (or a variant of that game)
       Arguments: none     (prompted text doesn't count as an argument)
       Results: none       (printing doesn't count as a result)
    """
    user = input("Choose your weapon: ")
    comp = random.choice(['rock', 'paper', 'scissors'])
    print()

    print('The user chose', user)
    print('The computer chose', comp)
    print()

    if user == 'rock' and comp == 'scissors':
        print('You won! My scissors shattered against your rock.')

    elif user == 'rock' and comp == 'paper':
        print('You lost! My paper strangled your rock.')

    elif user == 'rock' and comp == 'rock':
        print('The match was led to a draw, try again!')

    if user == 'paper' and comp == 'rock':
        print('You won! Your paper covered my rock.')

    elif user == 'paper' and comp == 'paper':
        print('The match was led to a draw, try again!')

    elif user == 'paper' and comp == 'scissors':
        print('You lost! My scissors chopped up your paper.')

    if user == 'scissors' and comp == 'rock':
        print('You lost! My rock beat your scissors to smithereens.')

    elif user == 'scissors' and comp == 'paper':
        print('You won! Your scissors chopped up my paper.')

    elif user == 'scissors' and comp == 'scissors':
        print('The match was led to a draw, try again!')

        
   

    print("Thanks for playing!")

rps()