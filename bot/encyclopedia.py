import json
from discord.ext import commands
import os

class Encyclopedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMember = None
        
    @commands.command(help = "")
    async def addentry(self, ctx, name: str, *, description: str):
        f = open(format_path(ctx.guild.id), "r+")
        table = json.loads(f.read())
        table.update({name:description})
        f.seek(0)
        f.truncate()
        f.write(json.dumps(table))
        f.close()
        await ctx.send("Item added")
    
    @commands.command(help = "")
    async def removeentry(self, ctx, name: str):
        f = open(format_path(ctx.guild.id), "r+")
        table = json.loads(f.read())
        if name in table.keys():
            del table[name]
        else:
            f.close()
            await ctx.send("Item is not in table")
            return
        f.seek(0)
        f.truncate()
        f.write(json.dumps(table))
        f.close()
        await ctx.send("Item removed")
        
    @commands.command(help = "")
    async def showencyclopedia(self, ctx):
        f = open(format_path(ctx.guild.id), "r")
        table = json.loads(f.read())
        display_string = "```"
        for name in table.keys():
            display_string += (f"\n{name}")
        display_string += "```"
        await ctx.send(display_string)
    
    @commands.command(help = "")
    async def showentry(self, ctx, name: str):
        f = open(format_path(ctx.guild.id), "r")
        table = json.loads(f.read())
        f.close()
        display_string = ""
        if name in table.keys():
            display_string = (f"**{name}:**\n{table.get(name)}")
        else:
            display_string = "There is no such item."
        await ctx.send(display_string)
    
    
    
    
def format_path(id):
    return(f"./servers/{id}/encyclopedia.json")
