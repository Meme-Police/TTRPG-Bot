from discord.ext import commands
import os
import logging as log
import init_table

# TODO: Write initiative help
init_help = '''Add entity to initiative table.
Providing the initiative is required.
This number may not be negative.
Providing a name is optional. If no name is provided, your server nickname will be used'''

manual_table_create_help = '''A one time command to create the initiave table file for your server.
The bot keeps track of initiative using a text file.
The bot should have automatically created this file when it joined your server.
If it did not, then you will need to call this command.'''

removeinit_help = '''Remove entity from initiative table.
Providing a name is not required.
Not providing a name will remove yourself from the initiative table.
'''
displayinit_help = '''Displays the initiative table'''

clearinit_help = '''Clears the initiative table'''

nextturn_help = '''Jumps to and displays the next player/s on the initiative table.'''

thisturn_help = '''Shows all players at the current initiative.'''



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
    async def addinit(self, ctx, initiative: int, name: str = "-1"):
        if (initiative < 1):
            await ctx.send("You're so slow the table can't keep track of you.")
            return
        ent_name = name
        if (ent_name == "-1"):
            ent_name = ctx.author.display_name
        log.debug(ent_name)
        init_path = format_path(ctx.guild.id)
        if (os.path.exists(init_path) != True):
            await ctx.send("It looks like I don't have an initiative file for this server. You found a rare bug! Please type '|manualtablecreate' to fix this issue")
            return
        f = open(init_path, "r+")
        init_object = init_table.fromJson(f.read())
        init_object.insert(ent_name, initiative)
        f.seek(0)
        f.truncate()
        f.write(init_object.toJson())
        f.close()
        await ctx.send(f"Added {ent_name} with an initiative of {initiative}")
    
    
    @commands.command(help = removeinit_help)
    async def removeinit(self, ctx, name: str = "-1"):
        ent_name = name
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
    
    
    @commands.command(help = displayinit_help)
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
    
    @commands.command(help = clearinit_help)
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
        await ctx.send("Initiative has been cleared")
    
    # TODO: Write help text
    @commands.command(help = nextturn_help)
    async def nextturn(self, ctx):
        init_path = format_path(ctx.guild.id)
        if (os.path.exists(init_path) != True):
            await ctx.send("It looks like I don't have an initiative file for this server. You found a rare bug! Please type '|manualtablecreate' to fix this issue")
            return
        f = open(init_path, "r+")
        init_object = init_table.fromJson(f.read())
        players = init_object.next()
        f.seek(0)
        f.truncate()
        f.write(init_object.toJson())
        f.close
        player_string = ",".join(players)
        player_string.replace("'", "")
        await ctx.send(player_string)
    
    # TODO: Write help text
    @commands.command(help = thisturn_help)
    async def thisturn(self, ctx):
        init_path = format_path(ctx.guild.id)
        if (os.path.exists(init_path) != True):
            await ctx.send("It looks like I don't have an initiative file for this server. You found a rare bug! Please type '|manualtablecreate' to fix this issue")
            return
        f = open(init_path, "r")
        init_object = init_table.fromJson(f.read())
        f.close()
        players = init_object.current()
        player_string = ",".join(players)
        player_string.replace("'", "")
        if(player_string == ""):
            player_string == "It is currently no one's turn, type '|nextturn' to go to the next players turn."
        await ctx.send(player_string)
        
        
        
def format_path(server):
    return (f"./servers/{server}/initiative.json")
        
    
        
        
        
