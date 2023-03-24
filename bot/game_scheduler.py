import schedule
import re
from discord.ext import commands
import functools
import asyncio
import threading
import time
no_argument_list = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "day", "days", "week", "weeks", "seconds"]
has_argument_list = ["at", "every"]

def real_pop(list, n):
    for x in range(n):
        list.pop()
    return

def schedule_string_builder(job, string_list):
    #if job == None:
       #if time_string in no_argument_list:
            #return getattr(schedule, time_string)
        #elif time_string in has_argument_list:
            #return getattr(schedule, time_string)(extra)
    #else:
        #if time_string in no_argument_list:
            #return getattr(job, time_string)
        #elif time_string in has_argument_list:
            #return getattr(job, time_string)(extra)
    
    # For daily jobs -> `HH:MM:SS` or `HH:MM`
    if string_list == []:
        return job
    if job == None:
        job = schedule
    if string_list[-1] in no_argument_list:
        return schedule_string_builder(getattr(job, string_list.pop()), string_list)
    elif string_list[-1] in has_argument_list:
        if len(string_list) == 1:
            return schedule_string_builder(getattr(job, string_list.pop()), string_list)
        elif re.match("[0-9]{2}:[0-9]{2}", string_list[-2]):
            return schedule_string_builder(getattr(job, string_list.pop())(string_list.pop()), string_list)
        elif re.match("[0-9]", string_list[-2]):
            return schedule_string_builder(getattr(job, string_list.pop())(int(string_list.pop())), string_list)


class GameScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMember = None
    
    @commands.command(help = "")
    async def makereminder(self, ctx, *, time: str):
        args = time.split(" ")
        args.reverse()
        
        # Surround with try catch
        job = schedule_string_builder(None, args)
        
        dmChannel = await ctx.message.author.create_dm()
        def check(msg):
            return msg.author == ctx.author and msg.channel == dmChannel
        
        await ctx.author.send("Please enter a name for the reminder,\nThis will be used to help manage your reminders.")
        msg = await self.bot.wait_for("message", check = check, timeout = 90)
        first_word = msg.content.split(" ")[0]
        job = job.tag(first_word, str(str(ctx.guild.id)+first_word), str(ctx.guild.id))
        def _task():
            asyncio.run_coroutine_threadsafe(ctx.send("This is the message"), self.bot.loop)
        job.do(functools.partial(_task))

        print(schedule.get_jobs())
    
    @commands.command(help = "")
    async def viewreminders(self, ctx):
        jobs = schedule.get_jobs(str(ctx.guild.id))
        display_string = "```"
        for job in jobs:
            regex = re.compile(f"{ctx.guild.id}")
            name = str([x for x in list(job.tags) if not regex.match(x)][0])
            display_string += name
        display_string += "```"
        await ctx.send(display_string)
    
    @commands.command(help = "")
    async def removereminder(self, ctx, reminder_name: str):
        schedule.clear((str(ctx.guild.id)+reminder_name))
 
#this function is from the "schedule" doccumentation at https://schedule.readthedocs.io/en/stable/background-execution.html        
def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

run_continuously()
                
        