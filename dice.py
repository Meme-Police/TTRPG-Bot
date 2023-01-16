import random
import functools

# This will return a tuple of the individual rolls, as well as the total
def roll(string):
    string = string.lower()
    (number, sides) = tuple(string.split('d'))
    if number == '':
        number = 1
    rolls = []
    for x in range(int(number)):
        rolls.append(random.randint(1, int(sides)))
    return (rolls, functools.reduce(lambda a, b: a+b, rolls))

    