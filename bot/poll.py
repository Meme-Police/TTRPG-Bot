from discord.ext import commands
import asyncio

poll_help = "Initiates a DM with the bot to create a poll\nCall the command in the channel you want the poll to be in, then create the poll in the DM."
reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMember = None
    
    @commands.command(help = poll_help)
    async def makepoll(self, ctx):
        not_done = True
        # Like slack, the ID of a direct message channel is different than the ID of the user, even though you can send a message via user id.
        dmChannel = await ctx.message.author.create_dm()
        element_list = []
        def check(msg):
            return msg.author == ctx.author and msg.channel == dmChannel
        try:
            poll_string = "```"
            while(not_done):
                await ctx.author.send("Enter the text for a single option. Or type '|done' to complete the poll.")
                msg = await self.bot.wait_for("message", check = check, timeout = 90)
                if (msg.content == "|done"):
                    not_done = False
                else:
                    element_list.append(msg.content)
                    if (len(element_list) == 10):
                        not_done = False
            
            for i in range(len(element_list)):
                poll_string += (f"\n{i+1}: {element_list[i]}")
            poll_string += "```"
            message = await ctx.send(poll_string)
            for i in range(len(element_list)):
                await message.add_reaction(reactions[i])
                
        except asyncio.TimeoutError as e:
            await ctx.author.send("You took to long. I have a small brain and can't hold onto this.\nYou can try again when you're ready.\nJust remember to call the command in the channel you want the poll to be in.")
            
            