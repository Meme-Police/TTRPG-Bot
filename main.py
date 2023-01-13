import discord
import asyncio

token = open("token.txt").read()

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    channels = client.get_all_channels()
    await list(channels)[2].send("I am here")

asyncio.get_event_loop().run_until_complete(client.run(token))