from discord.ext import commands
import logging as log
import os
import member

set_health_help = '''Sets your max health.
<a> must be an integer (a whole number)
Examples: 
            |sethealth 100
            |sethealth 77
            |sethealth 0'''

class PlayerManagment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMember = None

    @commands.command(help = set_health_help)
    async def sethealth(self, ctx, a: int, b: str = "-1"):
        
        user_path = ""
        if (b == "-1"):
            user_path = format_path(ctx.guild.id, ctx.author.id)
        else:
                user_path = format_path(ctx.guild.id, b[2:-1])
        
        if (os.path.exists(user_path) != True):
            await ctx.send("It looks like you, or the user you specified, needs to register to use that command.\nType '|register' to register")
            return
        f = open(user_path, 'r+')
        member_object = member.fromJson(f.read())
        member_object.max_health = a
        if (member_object.max_health < member_object.health):
            member_object.health = a
            await ctx.send(f"Max health is now {a}, since this was below their current health, it has been lowered to match their max health.")
        else:    
            await ctx.send(f"Max health is now {a}, but that players current health will remain at {member_object.health} untill changed")
        f.seek(0)
        f.truncate()
        f.write(member_object.toJson())
        f.close()
        
    # TODO: Damage Command
    
    # TODO: Heal Command
    
    # TODO: Check Health Command
    
    # TODO: Set Spell Command
    
    # TODO: Use Spell Command
    
    # TODO: Restore Spell Command
    
    # TODO: Check Spells Command
    
    # TODO: Long Rest Command
        
        

def format_path(server, user):
    return (f"./servers/{server}/users/{user}.json")