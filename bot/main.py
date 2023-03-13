import discord
from discord.ext import commands
from discord.ext.commands import errors
import dice
import registration
import logging as log
import player_managment
import initiative
import encounter
import shop

intents = discord.Intents.default()

token = open("token.txt").read()

bot = commands.Bot(command_prefix='|', intents = intents)


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))
    # Adding the cogs
    bot.add_cog(dice.Roll(bot))
    bot.add_cog(registration.Registrastion(bot))
    bot.add_cog(player_managment.PlayerManagment(bot))
    bot.add_cog(initiative.Initiative(bot))
    bot.add_cog(encounter.Encounter(bot))
    bot.add_cog(shop.Shop(bot))
    

#This will be called any time there is an error before the command function is run
@bot.event
async def on_command_error(ctx, error):
    log.warning(error.__class__.__name__)
    if (isinstance(error, discord.ext.commands.errors.MissingRequiredArgument)):
        await ctx.send(f"This command requires additional information.\nType '|help {ctx.invoked_with}' for more info.")
    elif (isinstance(error, discord.ext.commands.errors.BadArgument)):
        await ctx.send(f"I didn't understand your input.\nTry typing '|help {ctx.invoked_with}' to see what kind of input is valid.")
    elif (isinstance(error, discord.ext.commands.errors.CommandNotFound)):
        # A command not found error can be raised for a number of reasons. 
        # While it's possible for a user can cause this error by mispelling a command.
        # It's also possible for another bot on the server to utilize the same command prefix.
        # In this instance we do not want our bot to reply, even with an error, if a user is trying to use the command of another bot.
        pass
    else:
        log.error(error)
        await ctx.send(f"I encountered a {ctx.invoked_with} error. I wasn't expecting this and I don't know how to handle it.")

bot.run(token)