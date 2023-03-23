import schedule
import re
from discord.ext import commands
import functools
import asyncio
import threading
import time
no_argument_list = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "day", "days", "week", "weeks", "seconds"]
has_argument_list = ["at", "every"]

def schedule_string_builder(job, time_string, extra = 1):
    if job == None:
        if time_string in no_argument_list:
            return getattr(schedule, time_string)
        elif time_string in has_argument_list:
            return getattr(schedule, time_string)(extra)
    else:
        if time_string in no_argument_list:
            return getattr(job, time_string)
        elif time_string in has_argument_list:
            return getattr(job, time_string)(extra)


class GameScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastMember = None
    
    @commands.command(help = "")
    async def makenotification(self, ctx, *, time: str):
        args = time.split(" ")
        job = None
        i = 0
        while i < (len(args) - 1):
            if re.match("[0-9]", args[i+1]):
                job = schedule_string_builder(job, args[i], int(args[i+1]))
                i += 2
            else:
                job = schedule_string_builder(job, args[i])
                i += 1
        if i < len(args):
            job = schedule_string_builder(job, args[i])
        
        def _task():
            asyncio.run_coroutine_threadsafe(ctx.send("This is the message"), self.bot.loop)
        job.do(functools.partial(_task))

        print(schedule.get_jobs())
        
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
                
        