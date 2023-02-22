import json
from discord.ext import commands
import os
import encounter_table

class Encounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMember = None
    
    # TODO: Write help text
    # Also TODO: come up with a better command name
    @commands.command(help = "")
    async def createencountertable(self, ctx, table_name: str):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path)):
            await ctx.send(f"That table already exists. To delete it, type '|deleteencountertable {table_name}'.")
            return
        f = open(path, "w")
        f.write(encounter_table.EncounterTable({}, ctx.author.id).toJson())
        f.close()
        await ctx.send(f"Table {table_name} created.")
    
    @commands.command(help = "")
    async def deleteencountertable(self, ctx, table_name: str):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path) == False):
            await ctx.send(f"That table doesn't exists. To create it, type '|createencountertable {table_name}'.")
            return
        f = open(path, "r")
        table_object = encounter_table.fromJson(f.read())
        f.close()
        if (table_object.owner == ctx.author.id):
            os.remove(path)
            await ctx.send(f"Table {table_name} has been deleted.")
        else:
            await ctx.send("It looks like you don't own that table.\nYou can't delete a table unless you own it.")
        
    
def format_path(server, name):
    return (f"./servers/{server}/encounter_tables/{name}.json")