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
    async def createtable(self, ctx, table_name: str):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path)):
            await ctx.send(f"That table already exists. To delete it, type '|deletetable {table_name}'.")
            return
        f = open(path, "w")
        f.write(encounter_table.EncounterTable({}, ctx.author.id).toJson())
        f.close()
        await ctx.send(f"Table {table_name} created.")
    
    @commands.command(help = "")
    async def deletetable(self, ctx, table_name: str):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path) == False):
            await ctx.send(f"That table doesn't exists. To create it, type '|createtable {table_name}'.")
            return
        f = open(path, "r")
        table_object = encounter_table.fromJson(f.read())
        f.close()
        if (table_object.owner == ctx.author.id):
            os.remove(path)
            await ctx.send(f"Table {table_name} has been deleted.")
        else:
            await ctx.send("It looks like you don't own that table.\nYou can't delete a table unless you own it.")
            
    # TODO: Create item
    @commands.command(help = "")
    async def addencounter(self, ctx, table_name: str, *, description: str):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path) == False):
            await ctx.send(f"That table doesn't exists. To create it, type '|createtable {table_name}'.")
            return
        f = open(path, "r+")
        table_object = encounter_table.fromJson(f.read())
        if (table_object.owner == ctx.author.id):
            table_object.addItem(description)
            f.seek(0)
            f.truncate()
            f.write(table_object.toJson())
            f.close()
            await ctx.send("Item added")
        else:
            await ctx.send("You are not the owner of that table.")
    
    # TODO: Remove item
    async def deleteencounter(self, ctx, table_name: str, item_number: int):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path) == False):
            await ctx.send(f"That table doesn't exists. To create it, type '|createtable {table_name}'.")
            return
        f = open(path, "r+")
        table_object = encounter_table.fromJson(f.read())
        if (table_object.owner == ctx.author.id):
            table_object.removeItem(item_number)
            f.seek(0)
            f.truncate()
            f.write(table_object.toJson())
            f.close()
            await ctx.send("Item removed")
        else:
            await ctx.send("You are not the owner of that table.")
    
    @commands.command(help = "")
    async def showtable(self, ctx, table_name: str):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path) == False):
            await ctx.send(f"That table doesn't exists. To create it, type '|createtable {table_name}'.")
            return
        f = open(path, "r")
        table_object = encounter_table.fromJson(f.read())
        if (table_object.owner == ctx.author.id):
            await ctx.send(table_object.displayTable())
            pass
        else:
            await ctx.send("You are not the owner of that table.")
        
    
def format_path(server, name):
    return (f"./servers/{server}/encounter_tables/{name}.json")