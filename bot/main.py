import discord
from discord.ext import commands
import dice
import registration

intents = discord.Intents.default()

token = open("token.txt").read()

bot = commands.Bot(command_prefix='|', intents = intents)


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))
    # Adding the cogs
    bot.add_cog(dice.Roll(bot))
    bot.add_cog(registration.Registrastion(bot))

bot.run(token)