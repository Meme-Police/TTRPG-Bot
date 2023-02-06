from discord.ext import commands
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMember = None
    
    @commands.command()
    async def help(self, ctx, com: str = None):
        try:
            message = ""
            if com == None:
                for command_name in self.bot.commands:
                    message += "|{command_name}\n"
                await ctx.send(message)
        except:
            await ctx.send("Oopsiedoodle, I had trouble with the help command")