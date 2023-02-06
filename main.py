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
    bot.add_cog(dice.Roll(bot))

bot.run(token)