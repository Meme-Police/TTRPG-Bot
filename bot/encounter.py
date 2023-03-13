import json
from discord.ext import commands
import os
import encounter_table

createtable_help = '''Creates a blank encounter table
<table_name> The name for the table. CANNOT CONTAIN SPACES.
Examples:
            |createtable MyEncounterTable
            |createtable ForestEncounters'''
deletetable_help = '''Deletes a table.
You must be the creator of the table to delete it.
<table_name> The name of the table to delete. Will return an error if the table does not exist.
Examples:
            |deletetable MyEncounterTable
            |deletetable ForestEncounters'''
addencounter_help = '''Adds an encounter to an encounter table.
You must be the creator of a table to add an encounter to it.
<table_name> The name of the table.
<description> The text of the encounter. May contain spaces (wouldn't be a very usefull feature otherwise XD)
Example:
            |addencounter ForrestEncounters The party hears a loud roar quickely folllowed by a flock of birds quickly exiting the treetops...'''
deleteencounter_help = '''Deletes an encounter.
This one is a bit tricky as I don't expect you to put in the whole description of the encounter word for word.
Instead you must provide the number of the encounter in the list.
You can find the number of the encounter you want to remove by using the showtable command.
<table_name> The name of the table
<item_numner> The number of the item to delete
Examples:
            |deleteencounter ForestEncounters 2
            |deleteencounter MyEncounterTable 1
'''
showtable_help = '''Shows an encounter table.
You must be the creator of the table to view it.
<table_name> The name of the table
Example:
            |showtable ForestEncounters'''
rolltable_help = '''Selects a random encounter from an encounter table.
You must be the creator of the table to use this function.
<table_name> The name of the table.
Example:
            |rolltable ForestEncounters'''

class Encounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMember = None
    
    # TODO: Write help text
    @commands.command(help = createtable_help)
    async def createtable(self, ctx, table_name: str):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path)):
            await ctx.send(f"That table already exists. To delete it, type '|deletetable {table_name}'.")
            return
        f = open(path, "w")
        f.write(encounter_table.EncounterTable([], ctx.author.id).toJson())
        f.close()
        await ctx.send(f"Table {table_name} created.")
    
    @commands.command(help = deletetable_help)
    async def deletetable(self, ctx, table_name: str):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path) == False):
            await ctx.send(f"That table doesn't exist. To create it, type '|createtable {table_name}'.")
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
    @commands.command(help = addencounter_help)
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
    @commands.command(help = deleteencounter_help)
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
    
    @commands.command(help = showtable_help)
    async def showtable(self, ctx, table_name: str):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path) == False):
            await ctx.send(f"That table doesn't exists. To create it, type '|createtable {table_name}'.")
            return
        f = open(path, "r")
        table_object = encounter_table.fromJson(f.read())
        if (table_object.owner == ctx.author.id):
            await ctx.author.send(table_object.displayTable())
            pass
        else:
            await ctx.send("You are not the owner of that table.")
    
    @commands.command(help = rolltable_help)
    async def rolltable(self, ctx, table_name: str):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path) == False):
            await ctx.send(f"That table doesn't exists. To create it, type '|createtable {table_name}'.")
            return
        f = open(path, "r")
        table_object = encounter_table.fromJson(f.read())
        if (table_object.owner == ctx.author.id):
            await ctx.author.send(table_object.choseItem())
            pass
        else:
            await ctx.send("You are not the owner of that table.")
        
    
def format_path(server, name):
    return (f"./servers/{server}/encounter_tables/{name}.json")