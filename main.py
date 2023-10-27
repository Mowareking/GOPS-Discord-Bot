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
            opponent_author = client.get_user(opponent_id)
            opponent_mention = message.content[6:-1] + ">"

            await message.channel.send(opponent_mention + " Do you want to play?\nYes/No")
            try:
                opponent_message = await client.wait_for("message", check=lambda reply: reply.content.lower() in ["yes", "no"] and reply.author.id == opponent_id and reply.channel == message.channel, timeout=60.0)
            except asyncio.TimeoutError:
                 return await message.channel.send(f'Sorry, {opponent_mention} took too long to respond.')

            if opponent_message.content.lower() == "yes":
                 await message.channel.send(f"{message.author.mention}, {opponent_mention} The game is starting!")
            if opponent_message.content.lower() == "no":
                 await message.channel.send("Game over.")

            author_hand, opponent_hand, stock = [x for x in range(1, 14)], [x for x in range(1, 14)], [x for x in range(1, 14)]
            author_prizes, opponent_prizes = [], []
            random.shuffle(stock)
            upturned = []

            for i in range(13):
                upturned.append(stock.pop())
                cards_remaining = len(stock)
                author_move, opponent_move = "", ""
                
                await message.channel.send(f"Upturned card(s): {upturned}.\n{message.author.mention}'s prizes: {author_prizes}\n{opponent_mention}'s prizes: {opponent_prizes}\nCards remaining in deck: {cards_remaining}")
                await message.author.send(f"Upturned card(s): {upturned}.\nYour hand: {author_hand}\nYour prizes: {author_prizes}\n{opponent_mention}'s prizes: {opponent_prizes}\nCards remaining in deck: {cards_remaining}")
                await opponent_author.send(f"Upturned card(s): {upturned}.\nYour hand: {opponent_hand}\nYour prizes: {opponent_prizes}\n{message.author.mention}'s prizes: {author_prizes}\nCards remaining in deck: {cards_remaining}")

                while not opponent_move or not author_move:
                    try:
                        first_move = await client.wait_for("message", check=lambda reply: reply.author.id in [message.author.id, opponent_id] and not reply.guild, timeout=60.0)
                        if first_move.author.id == message.author.id and int(first_move.content) in author_hand:
                            await message.author.send(f"You have chosen your {first_move.content}")
                            author_move = first_move
                            break
                        elif first_move.author.id == opponent_id and int(first_move.content) in opponent_hand:
                            await opponent_author.send(f"You have chosen your {first_move.content}")
                            opponent_move = first_move
                            break
                        else:
                            await first_move.author.send("Invalid move")
                    except asyncio.TimeoutError:
                        return await message.channel.send(f'Sorry, the move took too long.')
                    
                while not opponent_move:
                    try:
                        opponent_move = await client.wait_for("message", check=lambda reply: reply.author.id == opponent_id and not reply.guild, timeout=120.0)
                        if int(opponent_move.content) in opponent_hand:
                            await opponent_author.send(f"You have chosen your {opponent_move.content}.")
                        else:
                            await opponent_author.send("Invalid move")
                            opponent_move = ""
                    except asyncio.TimeoutError:
                        return await message.channel.send(f'Sorry, the move took too long.')
                
                while not author_move:
                    try:
                        author_move = await client.wait_for("message", check=lambda reply: reply.author.id == message.author.id and not reply.guild, timeout=120.0)
                        if int(author_move.content) in author_hand:
                            await message.author.send(f"You have chosen your {author_move.content}.")
                        else:
                            await message.author.send("Invalid move")
                            author_move = ""
                    except asyncio.TimeoutError:
                        return await message.channel.send(f'Sorry, the move took too long.')
                
                opponent_move = int(opponent_move.content)
                author_move = int(author_move.content)
                opponent_hand.remove(opponent_move)
                author_hand.remove(author_move)

                await message.channel.send(f"{message.author.mention} played a {author_move}.\n{opponent_mention} played a {opponent_move}.")
                await message.author.send(f"{message.author.mention} played a {author_move}.\n{opponent_mention} played a {opponent_move}.")
                await opponent_author.send(f"{message.author.mention} played a {author_move}.\n{opponent_mention} played a {opponent_move}.")
                if author_move > opponent_move:
                    await message.channel.send(f"{message.author.mention} wins the prize(s)!")
                    await message.author.send("You won the prize(s)!")
                    await opponent_author.send("They won the prize(s)!")
                    author_prizes.extend(upturned)
                    upturned = []
                elif opponent_move > author_move:
                    await message.channel.send(f"{opponent_mention} wins the prize(s)!")
                    await message.author.send("They won the prize(s)!")
                    await opponent_author.send("You won the prize(s)!")
                    opponent_prizes.extend(upturned)
                    upturned = []
                elif opponent_move == author_move:
                    await message.channel.send("It's a tie!")
                    await message.author.send("It's a tie!")
                    await opponent_author.send("It's a tie!")
                else:
                    await message.channel.send("I am in error help pls")

            author_score = sum(author_prizes)
            opponent_score = sum(opponent_prizes)
            result = author_score - opponent_score
            await message.channel.send(f"{message.author.mention} final score: {author_score}\n{opponent_mention} final score: {opponent_score}")
            if result > 0:
                await message.channel.send(f"{message.author.mention} wins the game by {result}!!!")
            elif result < 0:
                result *= -1
                await message.channel.send(f"{opponent_mention} wins the game by {result}!!!")
            else:
                await message.channel.send(f"Both players tied somehow!")


                

client.run("MTE2NzE2NzM1NDk4MDAxNjIwMw.GphUqg.KmLq7KsnJTpv_pcDDTBqMXebGES-x1fopt7tS4")
