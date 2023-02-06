import random
import functools
from discord.ext import commands
import re

# This will return a tuple of the individual rolls, as well as the total
class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMember = None
    
    # Note to self: All member functions must include self as a parameter.   

    @commands.command(help = "Rolls a dice")
    async def roll(self, ctx, a: str):
        try:
            rolls = re.findall("[0-9]*[dD]{1}[0-9]+", a)
            # TODO: Remove Print
            print(rolls)
            results = []
            numbers = []
            for die in rolls:
                print(die)
                die_roll = make_roll(die)
                numbers.append(die_roll[0])
                results.append(die_roll[1])
                a = a.replace(die, str(results[-1]))
            # TODO: Remove Print
            print(results)
            print(a)
            await ctx.send("Total: " + str(eval(a)) + " Rolls: " + str(numbers))
        except Exception as e:
            print(e)
            await ctx.send("I am dumb and did not understand that.")
        
            
def make_roll(string):
    string = string.lower()
    (number, sides) = tuple(string.split('d'))
    if number == '':
        number = 1
    rolls = []
    for x in range(int(number)):
        rolls.append(random.randint(1, int(sides)))
    return (rolls, functools.reduce(lambda a, b: a+b, rolls))
    


    