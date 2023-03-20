from discord.ext import commands
import os
import shop_table

createtable_help = '''Creates a blank shop table
<table_name> The name for the table. CANNOT CONTAIN SPACES.
Examples:
            |createshop MyShop
            |createshop Temshop'''
deletetable_help = '''Deletes a shop.
You must be the creator of the shop to delete it.
<table_name> The name of the shop to delete. Will return an error if the shop does not exist.
Examples:
            |deleteshop MyShop
            |deleteshop Temshop'''
addencounter_help = '''Adds an item to a shop.
You must be the creator of a shop to add an encounter to it.
<shop_name> the name of the shop
<item_name> The name of the item.
<item_price> The price of the item
<description> The descriptio of the item. May contain spaces (wouldn't be a very usefull feature otherwise XD)
Example:
            |addshopitem MyShop KillingEdge 900g Has a high critical hit ratio.'''
deleteencounter_help = '''Deletes a shop item.
This one is a bit tricky as I don't expect you to put in the whole description of the encounter word for word.
Instead you must provide the number of the item in the list.
You can find the number of the item you want to remove by using the showshop command.
<table_name> The name of the shop
<item_numner> The number of the item to delete
Examples:
            |deleteitem MyShop 1
'''
showtable_help = '''Shows a shop.
You must be the creator of the shop to show it.
<table_name> The name of the shop
Example:
            |showshop LabyrinthShop'''

            
            

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMember = None
        
# TODO: Write help text
    @commands.command(help = createtable_help)
    async def createshop(self, ctx, table_name: str):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path)):
            await ctx.send(f"That shop already exists. To delete it, type '|deleteshop {table_name}'.")
            return
        f = open(path, "w")
        f.write(shop_table.ShopTable([], ctx.author.id).toJson())
        f.close()
        await ctx.send(f"Shop {table_name} created.")
    
    @commands.command(help = deletetable_help)
    async def deleteshop(self, ctx, table_name: str):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path) == False):
            await ctx.send(f"That shop doesn't exists. To create it, type '|createshop {table_name}'.")
            return
        f = open(path, "r")
        table_object = shop_table.fromJson(f.read())
        f.close()
        if (table_object.owner == ctx.author.id):
            os.remove(path)
            await ctx.send(f"Shop {table_name} has been deleted.")
        else:
            await ctx.send("It looks like you don't own that shop.\nYou can't delete a table unless you own it.")
            
    # TODO: Create item
    @commands.command(help = addencounter_help)
    async def addshopitem(self, ctx, shop_name: str, item_name: str, item_price: str, *, description: str):
        path = format_path(ctx.guild.id, shop_name)
        if (os.path.exists(path) == False):
            await ctx.send(f"That shop doesn't exists. To create it, type '|createshop {shop_name}'.")
            return
        f = open(path, "r+")
        table_object = shop_table.fromJson(f.read())
        if (table_object.owner == ctx.author.id):
            table_object.addItem(item_name, item_price, description)
            f.seek(0)
            f.truncate()
            f.write(table_object.toJson())
            f.close()
            await ctx.send("Item added")
        else:
            await ctx.send("You are not the owner of that shop.")
    
    # TODO: Remove item
    @commands.command(help = deleteencounter_help)
    async def deleteitem(self, ctx, table_name: str, item_number: int):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path) == False):
            await ctx.send(f"That table doesn't exists. To create it, type '|createshop {table_name}'.")
            return
        f = open(path, "r+")
        table_object = shop_table.fromJson(f.read())
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
    async def showshop(self, ctx, table_name: str):
        path = format_path(ctx.guild.id, table_name)
        if (os.path.exists(path) == False):
            await ctx.send(f"That table doesn't exists. To create it, type '|createtable {table_name}'.")
            return
        f = open(path, "r")
        table_object = shop_table.fromJson(f.read())
        if (table_object.owner == ctx.author.id):
            await ctx.send(table_object.displayTable())
            pass
        else:
            await ctx.send("You are not the owner of that table.")
    
    @commands.command(help = "Shows all shops you have created")
    async def allshops(self, ctx):
        path = (f"./servers/{ctx.guild.id}/shops/")
        shops = os.listdir(path)
        if (len(shops) == 0):
            await ctx.send("There are no shops, try making one with '|createshop <shop_name>'.")
        else:
            display_string = ""
            for shop in shops:
                display_string += (f"\n{shop[:-5]}")
            await ctx.send(display_string)
    

        
    
def format_path(server, name):
    return (f"./servers/{server}/shops/{name}.json")    