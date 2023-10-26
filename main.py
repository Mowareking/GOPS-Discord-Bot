import discord
import random
import asyncio

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$gops'):
            if len(message.content) < 7:
                if message.content[6] == " ":
                    return
            opponent_id = int(message.content[8:-1])
            opponent_mention = message.content[6:-1] + ">"
            await message.channel.send(opponent_mention + " Do you want to play?\nYes/No")
            try:
                opponent_message = await client.wait_for("message", check=lambda reply: reply.content.lower() in ["yes", "no"] and reply.author.id == opponent_id and reply.channel == message.channel, timeout=10.0)
            except asyncio.TimeoutError:
                 return await message.channel.send(f'Sorry, {opponent_mention} took too long to respond.')
            print("test 1 pass")
            if opponent_message.content.lower() == "yes":
                 await message.channel.send(f"{message.author.mention}, {opponent_mention} The game is starting!")
            if opponent_message.content.lower() == "no":
                 await message.channel.send("Game over.")


client.run("MTE2NzE2NzM1NDk4MDAxNjIwMw.GphUqg.KmLq7KsnJTpv_pcDDTBqMXebGES-x1fopt7tS4")
