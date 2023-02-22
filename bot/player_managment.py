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
    async def sethealth(self, ctx, a: int, b: str = "self"):
        
        user_path = ""
        if (b == "self"):
            user_path = format_path(ctx.guild.id, ctx.author.id)
        else:
                user_path = format_path(ctx.guild.id, b[2:self])
        
        if (os.path.exists(user_path) != True):
            await ctx.send("Either you need to register, or you tried to set someone elses health improperly.\nWhen trying to edit someone elses health, make sure to @ them in chat instead of typing their user name.")
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
        
    # TODO: Help Text
    @commands.command(help = "")
    async def damage(self, ctx, value: int, name: str = "self"):
        user_path = ""
        if (name == "self"):
            user_path = format_path(ctx.guild.id, ctx.author.id)
        else:
                user_path = format_path(ctx.guild.id, name[2:self])
        
        if (os.path.exists(user_path) != True):
            await ctx.send("Either you need to register, or you tried to set someone elses health improperly.\nWhen trying to edit someone elses health, make sure to @ them in chat instead of typing their user name.")
            return
        f = open(user_path, 'r+')
        member_object = member.fromJson(f.read())
        member_object.health -= value
        if (member_object.health <= 0):
            excess_damage = abs(member_object.health)
            member_object.health = 0
            await ctx.send(f"You have reached 0 hit points. You took {excess_damage} extra damage.")
        else: 
            await ctx.send(f"You are now at {member_object.health} hit points.")
        f.seek(0)
        f.truncate()
        f.write(member_object.toJson())
        f.close()
        
    
    # TODO: Heal Command help
    @commands.command(help = "")
    async def heal(self, ctx, value: int, name: str = "self"):
        user_path = ""
        if (name == "self"):
            user_path = format_path(ctx.guild.id, ctx.author.id)
        else:
                user_path = format_path(ctx.guild.id, name[2:self])
        
        if (os.path.exists(user_path) != True):
            await ctx.send("Either you need to register, or you tried to set someone elses health improperly.\nWhen trying to edit someone elses health, make sure to @ them in chat instead of typing their user name.")
            return
        f = open(user_path, 'r+')
        member_object = member.fromJson(f.read())
        member_object.health += value
        if (member_object.health >= member_object.max_health):
            member_object.health = member_object.max_health
        await ctx.send(f"You are now at {member_object.health} hit points.")
        f.seek(0)
        f.truncate()
        f.write(member_object.toJson())
        f.close()
    
    # TODO: Check Health Command
    @commands.command(help = "")
    async def viewhealth(self, ctx, name: str = "self"):
        user_path = ""
        if (name == "self"):
            user_path = format_path(ctx.guild.id, ctx.author.id)
        else:
                user_path = format_path(ctx.guild.id, name[2:self])
        if (os.path.exists(user_path) != True):
            await ctx.send("Either you need to register, or you tried to view someone elses health improperly.\nWhen trying to view someone elses health, make sure to @ them after the command instead of typing their username.")
            return
        f = open(user_path, "r")
        member_object = member.fromJson(f.read())
        f.close()
        await ctx.send(f"That person now has {member_object.health} hitpoints")
        return

    
    # TODO: Set Spell Command
    @commands.command(help = "")
    async def setspell(self, ctx, level: int, number_of_slots: int, name:str = "self"):
        user_path = ""
        if (name == "self"):
            user_path = format_path(ctx.guild.id, ctx.author.id)
        else:
                user_path = format_path(ctx.guild.id, name[2:self])
        if (os.path.exists(user_path) != True):
            await ctx.send("Either you need to register, or you tried to edit someone elses spell slots improperly.\nWhen trying to edit someone elses spell slots, make sure to @ them after the command instead of typing their username.")
            return
        f = open(user_path, "r+")
        member_object = member.fromJson(f.read())
        member_object.max_spells[level - 1] = number_of_slots
        f.seek(0)
        f.truncate()
        f.write(member_object.toJson())
        f.close()
        await ctx.send(f"That person now has {number_of_slots} level {level} spell slots")
        
    
    # TODO: Use Spell Command
    @commands.command(help = "")
    async def cast(self, ctx, level:int, name: str = "self"):
        user_path = ""
        if (name == "self"):
            user_path = format_path(ctx.guild.id, ctx.author.id)
        else:
            user_path = format_path(ctx.guild.id, name[2:self])
        if (os.path.exists(user_path) != True):
            await ctx.send("Either you need to register, or you tried to edit someone elses spell slots improperly.\nWhen trying to edit someone elses spell slots, make sure to @ them after the command instead of typing their username.")
            return
        f = open(user_path, "r+")
        member_object = member.fromJson(f.read())
        if (member_object.spells[level - 1] > 0):
            member_object.spells[level - 1] = member_object.spells[level - 1] - 1
            await ctx.send(f"You have {member_object.spells[level - 1]} level {level} spell slots remaining.")
        else:
            await ctx.send(f"You don't have any level {level} spell slots left. Go touch grass.")
        f.seek(0)
        f.truncate()
        f.write(member_object.toJson())
        f.close()
        
    # TODO: Restore Spell Command
    @commands.command(help = "")
    async def restoreslots(self, ctx, level: int, number_of_slots: int, name: str = "self"):
        user_path = ""
        if (name == "self"):
            user_path = format_path(ctx.guild.id, ctx.author.id)
        else:
            user_path = format_path(ctx.guild.id, name[2:self])
        if (os.path.exists(user_path) != True):
            await ctx.send("Either you need to register, or you tried to edit someone elses spell slots improperly.\nWhen trying to edit someone elses spell slots, make sure to @ them after the command instead of typing their username.")
            return
        f = open(user_path, "r+")
        member_object = member.fromJson(f.read())
        member_object.spells[level - 1] += number_of_slots
        if (member_object.spells[level - 1] > member_object.max_spells[level - 1]):
            member_object.spells[level - 1] = member_object.max_spells[level - 1]
            await ctx.send(f"You tried to restore {number_of_slots} level {level} spell slots, but that put you over your max slots for that level.")
        await ctx.send(f"You now have {member_object.spells[level - 1]} level {level} spell slots remaining.")
        f.seek(0)
        f.truncate()
        f.write(member_object.toJson())
        f.close()
        
    # TODO: Check Spells Command
    @commands.command(help = "")
    async def checkspells(self, ctx, name: str = "self"):
        user_path = ""
        if (name == "self"):
            user_path = format_path(ctx.guild.id, ctx.author.id)
        else:
            user_path = format_path(ctx.guild.id, name[2:self])
        if (os.path.exists(user_path) != True):
            await ctx.send("Either you need to register, or you tried to edit someone elses spell slots improperly.\nWhen trying to edit someone elses spell slots, make sure to @ them after the command instead of typing their username.")
            return
        f = open(user_path, "r")
        member_object = member.fromJson(f.read())
        f.close()
        spells_string = "```"
        level = 1
        for number in member_object.spells:
            spells_string += (f"\nLevel {level}: {number}")
            level += 1
        spells_string += "\n```"
        await ctx.send(spells_string)
    
    # TODO: Long Rest Command
    @commands.command(help = "")
    async def longrest(self, ctx, name: str = "self"):
        user_path = ""
        if (name == "self"):
            user_path = format_path(ctx.guild.id, ctx.author.id)
        else:
            user_path = format_path(ctx.guild.id, name[2:self])
        if (os.path.exists(user_path) != True):
            await ctx.send("Either you need to register, or you tried to edit someone elses spell slots improperly.\nWhen trying to edit someone elses spell slots, make sure to @ them after the command instead of typing their username.")
            return
        f = open(user_path, "r+")
        member_object = member.fromJson(f.read())
        member_object.health = member_object.max_health
        member_object.spells = member_object.max_spells
        f.seek(0)
        f.truncate()
        f.write(member_object.toJson())
        f.close()
        await ctx.send("Health and spell slots restored.")
        

def format_path(server, user):
    return (f"./servers/{server}/users/{user}.json")