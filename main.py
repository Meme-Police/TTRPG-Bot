import discord
from discord.ext import commands
import re
import dice

intents = discord.Intents.default()

token = open("token.txt").read()

bot = commands.Bot(command_prefix='|', intents = intents)


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))
    

@bot.command()
async def roll(ctx, a: str):
    try:
        rolls = re.findall("[0-9]*[dD]{1}[0-9]+", a)
        print(rolls)
        results = []
        numbers = []
        for die in rolls:
            die_roll = dice.roll(die)
            numbers.append(die_roll[0])
            results.append(die_roll[1])
            a = a.replace(die, str(results[-1]))
        print(results)
        print(a)
        await ctx.send("Total: " + str(eval(a)) + " Rolls: " + str(numbers))
    except:
        await ctx.send("I am dumb and did not understand that.")
    

        
    
bot.run(token)