from discord.ext import commands
import os
import logging as log
import init_table

# TODO: Write initiative help
init_help = ''''''

manual_table_create_help = '''A one time command to create the initiave table file for your server.
The bot keeps track of initiative using a text file.
The bot should have automatically created this file when it joined your server.
If it did not, then you will need to call this command.'''



class Initiative(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMember = None
        
    @commands.command(help = manual_table_create_help)
    async def manualtablecreate(self, ctx):
        
        try:
            os.makedirs(os.path.dirname(format_path(ctx.guild.id)), exist_ok = True)
            f = open(format_path(ctx.guild.id), "w")
            init_object = init_table.Table()
            f.seek(0)
            f.truncate()
            f.write(init_object.toJson())
            f.close()
        except Exception as e:
            log.error(e)
            await ctx.send("I ran into an error.\nThis command is not used to reset the table, but rather to initialize it if it doesn't already exist.\nThis command should never need to be called. If it does need to be called, it should only need to be called once.")
    
    @commands.command(help = init_help)
    async def addinit(self, ctx, a: int, b: str = "-1"):
        ent_name = b
        if (ent_name == "-1"):
            ent_name = ctx.author.display_name
        log.debug(ent_name)
        init_path = format_path(ctx.guild.id)
        if (os.path.exists(init_path) != True):
            await ctx.send("It looks like I don't have an initiative file for this server. You found a rare bug! Please type '|manualtablecreate' to fix this issue")
            return
        f = open(init_path, "r+")
        init_object = init_table.fromJson(f.read())
        init_object.insert(ent_name, a)
        f.seek(0)
        f.truncate()
        f.write(init_object.toJson())
        f.close()
        await ctx.send(f"Added {ent_name} with an initiative of {a}")
    
    # TODO: Add help text
    @commands.command(help = "")
    async def removeinit(self, ctx, a: str = "-1"):
        ent_name = a
        if (ent_name == "-1"):
            ent_name = ctx.author.display_name
        log.debug(ent_name)
        init_path = format_path(ctx.guild.id)
        if (os.path.exists(init_path) != True):
            await ctx.send("It looks like I don't have an initiative file for this server. You found a rare bug! Please type '|manualtablecreate' to fix this issue")
            return
        f = open(init_path, "r+")
        init_object = init_table.fromJson(f.read())
        init_object.remove(ent_name)
        f.seek(0)
        f.truncate()
        f.write(init_object.toJson())
        f.close()
        await ctx.send(f"Removed {ent_name}")
    
    # TODO: Add help text
    @commands.command(help = "")
    async def displayinit(self, ctx):
        init_path = format_path(ctx.guild.id)
        if (os.path.exists(init_path) != True):
            await ctx.send("It looks like I don't have an initiative file for this server. You found a rare bug! Please type '|manualtablecreate' to fix this issue")
            return
        f = open(init_path, "r")
        init_object = init_table.fromJson(f.read())
        init_string = init_object.toString()
        f.close()
        await ctx.send(init_string)
    
    # TODO: Add help text
    @commands.command(help = "")
    async def clearinit(self, ctx):
        init_path = format_path(ctx.guild.id)
        if (os.path.exists(init_path) != True):
            await ctx.send("It looks like I don't have an initiative file for this server. You found a rare bug! Please type '|manualtablecreate' to fix this issue")
            return
        f = open(init_path, "w")
        init_object = init_table.Table()
        f.seek(0)
        f.truncate()
        f.write(init_object.toJson())
        f.close()
        
        
def format_path(server):
    return (f"./servers/{server}/initiative.json")
        
    
        
        
        
