from random import randint ,choice

p = input("what is your name")
i = int(input("what is your age"))

number = randint(0,i)

print ("your number is", number)



lo = ["you will become rich","you will become famous","you will become homeless"]
selection = choice(lo)

print ("your fortune is....",selection) 