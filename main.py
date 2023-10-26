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
    if message.content.startswith('$play'):
            if message.content[6] == " ":
                return
            opponent_id = message.content[6:-1]
            print(opponent_id)
            await message.channel.send(opponent_id + "> Do you want to play?\nYes/No")
            try:
                opponent_message = await client.wait_for("message", check=lambda msg: msg.content.lower() in ["yes", "no"] and msg.author.id == opponent_id, timeout=5.0)
            except asyncio.TimeoutError:
                 return await message.channel.send(f'Sorry, {opponent_id}> took too long to respond.')
            print("test 1 pass")
            if opponent_message.content.lower() == "yes":
                 await message.channel.send(f"{message.author.mention}, {opponent_id} The game is starting!")
            if opponent_message.content.lower() == "no":
                 await message.channel.send("Game over.")
            """
            await message.channel.send('Guess a number between 1 and 3.')
            
            def is_correct(m):
                return m.author == message.author and m.channel == message.channel and m.content.isdigit()

            answer = random.randint(1, 3)

            try:
                guess = await client.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long it was {answer}.')

            if int(guess.content) == answer:
                await message.channel.send('You are right!')
            else:
                await message.channel.send(f'Oops. It is actually {answer}.')
            """

client.run("MTE2NzE2NzM1NDk4MDAxNjIwMw.GphUqg.KmLq7KsnJTpv_pcDDTBqMXebGES-x1fopt7tS4")