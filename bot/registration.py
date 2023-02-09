from discord.ext import commands
import logging as log
from member import Member
import os
import json

registration_help = "registers a user on the server\n Must be called by any user who wishes to use the bot's features \n Simply type '|register'"
class Registrastion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMember = None
    
    @commands.command(help = registration_help)
    async def register(self, ctx):
        user_path = format_path(ctx.guild.id, ctx.author.id)
        if(os.path.exists(user_path)):
            await ctx.send("It looks like I already have you in the system.\nTo wipe your profile, type '|unregister'")
            return
        new_member = Member(ctx.author.id, 10, [0 for x in range(9)])
        os.makedirs(os.path.dirname(user_path), exist_ok=True)
        with open(user_path, "w") as out:
            out.write(new_member.toJson())
            out.close
        await ctx.send("You're now registered in the system.")
    
    @commands.command()
    async def unregister(self, ctx):
        await ctx.send("Oh yeah this don't do anything yet")
        
def format_path(server, user):
    return (f"./servers/{server}/users/{user}.json")