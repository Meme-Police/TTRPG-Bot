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
            
damage_help = '''Damages the indicated player. (Yourself if no player specified)
Any damage that brings someone below 0 hitpoints will automatically set them to 0 hitpoints and state the amount of extra damage.
<a> must be an integer (a whole number)
<b> must be an @ to a user, or you may leave it blank to indicate yourself.
If you were trying to target a discord user named "Paperclip" The correct syntax would be @Paperclip
Examples:
            |damage 5
            |damage 17 @Paperclip

'''
heal_help = '''heals the indicated player. (Yourself if no player specified)
<value> must be an integer (a whole number)
<name> must be an @ to a user, or it may be left blank to indicate yourself.
If you were trying to target a discord user named "Paperclip" The correct syntax would be @Paperclip
Examples:
            |heal 5
            |heal 17 @Paperclip
'''
viewhealth_help = '''Views the health of the indicated player. (Yourself if no player specified)
<name> must be an @ to a user, or it may be left blank to indicate yourself.
If you were trying to target a discord user named "Paperclip" The correct syntax would be @Paperclip
Examples:
            |viewhealth
            |viewhealth @Paperclip
'''
setspell_help = '''Sets the amount of slots for a given spell
<level> must be a whole number from 1 to 9 representing the spell level
<number_of_slots> must be a whole number representing the number of slots you wish to have for that spell level
<name> must be an @ to a user, or it may be left blank to indicate yourself.
Examples:
            |setspell 1 4
            (gives yourself 4 level 1 spell slots)
            
            |setspell 9 1 @Paperclip
            (gives paperclip 1 level 9 spell slot)
'''
cast_help = '''Uses a spell of the given slot if avalible.
A special mesage will be returned if there are no slots left of that level
<level> must be a whole number from 1 to 9 representing the spell level.
<name> must be an @ to a user, or it may be left blank to indicate yourself.
Examples:
            |cast 5
            (atempts to use a level 5 spell slot from your spell slots)
            
            |case 2 @Paperclip
            (atempts to use one of Paperclip's level 2 spell slots)
'''
restore_slots_help = '''Restores a number of slots to the given spell level.
This cant raise your current slots above your maximum slots.
<level> must be a whole number from 1 to 9 representing the spell level
<number_of_slots> must be a whole number representing the number of slots you wish to have for that spell level
<name> must be an @ to a user, or it may be left blank to indicate yourself.
Examples:
            |restoreslots 1 4
            (restores 4 level 1 spell slots to yourself)
            
            |restoreslots 9 1 @Paperclip
            (restores 1 level 9 spell slot to paperclip)

'''
checkspells_help = '''Checks the number of spells avalible to the given player.
<name> must be an @ to a user, or it may be left blank to indicate yourself.
Examples: 
            |checkspells
            |checkspells @Paperclip
'''
longrest_help = '''Restores all health and spell slots to the indicated player.
<name> must be an @ to a user, or it may be left blank to indicate yourself.
Examples:
            |longrest
            |longrest @Paperclip
'''

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
    @commands.command(help = damage_help)
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
    @commands.command(help = heal_help)
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
    @commands.command(help = viewhealth_help)
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
    @commands.command(help = setspell_help)
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
    @commands.command(help = cast_help)
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
    @commands.command(help = restore_slots_help)
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
    @commands.command(help = checkspells_help)
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
    @commands.command(help = longrest_help)
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