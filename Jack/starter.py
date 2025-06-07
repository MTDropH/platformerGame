#Make a short program that assk the user for their name and age.

#It should then print out:
#- a random number less than the user's age
#- a randomly selected 'fortune' (like from a fortune cookie)

#Hints:
#Use the random module
#You could make a list of predictions then random.choice(list) to select one

import random

print("what is your age and name")

name = input("insert name here")

print("hello",name,"how old are you")

age = int(input("input age here"))

fortune = random.randint(0,age)

print("your fortune is",fortune)

l = []


