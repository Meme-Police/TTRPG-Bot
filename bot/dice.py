import random
import functools
from discord.ext import commands
import re
import logging as log

roll_help = "Rolls dice. \n Takes one argument <a> of standard dice notation. May be an equasion \n Examples: '|roll 3d10+2'\n           '|roll d20'\n           '|roll 13d24+81d7-4d3*2'"

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMember = None
    
    # Note to self: All member functions of the class must include self as a parameter.   

    @commands.command(help = roll_help)
    async def roll(self, ctx, dice_roll: str = "d20"):
        original_text = dice_roll
        try:
            rolls = parse_rolls(dice_roll)
            log.info(rolls)
            results = []
            numbers = []
            for die in rolls:
                print(die)
                die_roll = make_roll(die)
                numbers.append(die_roll[0])
                results.append(die_roll[1])
                dice_roll = dice_roll.replace(die, str(results[-1]))
            log.info(results)
            log.info(dice_roll)
            await ctx.send(f"{original_text}\nTotal: {str(eval(dice_roll))} Rolls: {str(numbers)}")
        except Exception as e:
            # TODO: this first log.error is used for debuging purposes as a way to use roll to view arbitrary message content
            # Remove in the future.
            log.error(ctx.message.content)
            log.error(e)
            await ctx.send("I am dumb and did not understand that.")

def parse_rolls(roll_string):
    return re.findall("[0-9]*[dD]{1}[0-9]+", roll_string)

# This will return a tuple of the individual rolls, as well as the total            
def make_roll(string):
    string = string.lower()
    (number, sides) = tuple(string.split('d'))
    if number == '':
        number = 1
    rolls = []
    for x in range(int(number)):
        rolls.append(random.randint(1, int(sides)))
    return (rolls, functools.reduce(lambda a, b: a+b, rolls))
    


    