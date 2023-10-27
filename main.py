import discord
import random
import asyncio

client = discord.Client(intents=discord.Intents.all())

def create_embed(desc, footer=None):
    embed = discord.Embed(
        colour=discord.Color.from_rgb(0, 0, 0),
        description=f"**{desc}**",
        title="Game of Pure Strategy"
    )
    if footer:
        embed.set_footer(text=footer)
    return embed

def create_card(cards, suit):
    
    for card in cards:


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

            await message.channel.send(embed=create_embed(f"{message.author.mention} :clubs: wants to play a game of GOPS. Do you accept?\nYes/No"))
            try:
                opponent_message = await client.wait_for("message", check=lambda reply: reply.content.lower() in ["yes", "no"] and reply.author.id == opponent_id and reply.channel == message.channel, timeout=60.0)
            except asyncio.TimeoutError:
                 return await message.channel.send(embed=create_embed(f'Sorry, {opponent_mention} took too long to respond.'))

            if opponent_message.content.lower() == "yes":
                 await message.channel.send(embed=create_embed(f"{message.author.mention}, {opponent_mention} The game is starting!"))
            if opponent_message.content.lower() == "no":
                 await message.channel.send(embed=create_embed("GOPS game offer denied."))

            author_hand, opponent_hand, stock = [str(x) for x in range(2, 11)], [str(x) for x in range(2, 11)], [str(x) for x in range(2, 11)]

            royals = ["A", "J", "Q", "K"]
            author_hand.insert(0, "A")

            author_hand.extend(royals[1:])
            opponent_hand.insert(0, "A")

            opponent_hand.extend(royals[1:])
            stock.insert(0, "A")

            stock.extend(royals)
            author_prizes, opponent_prizes = [], []
            random.shuffle(stock)
            upturned = []

            for i in range(13):
                upturned.append(stock.pop())
                cards_remaining = len(stock)
                author_move, opponent_move = "", ""
                
                """
                await message.channel.send(f"Upturned card(s): {upturned}.\n{message.author.mention}'s prizes: {author_prizes}\n{opponent_mention}'s prizes: {opponent_prizes}\nCards remaining in deck: {cards_remaining}")
                """

                upturned_display = str(upturned)[1:-1].replace("'", "")
                author_hand_display = str(author_hand)[1:-1].replace("'", "")
                opponent_hand_display = str(opponent_hand)[1:-1].replace("'", "")
                author_prizes_display = str(author_prizes)[1:-1].replace("'", "")
                opponent_prizes_display = str(opponent_prizes)[1:-1].replace("'", "")

                await message.author.send(embed=create_embed(f"Upturned card(s):  {upturned_display}\nYour hand:  {author_hand_display}\nYour prizes:  {author_prizes_display}\n{opponent_mention}'s prizes: {opponent_prizes_display}", f"Cards remaining in deck: {cards_remaining}"))
                await opponent_author.send(embed=create_embed(f"Upturned card(s):  {upturned_display}\nYour hand:  {opponent_hand_display}\nYour prizes:  {opponent_prizes_display}\n{message.author.mention}'s prizes: {author_prizes_display}", f"Cards remaining in deck: {cards_remaining}"))

                while not opponent_move or not author_move:
                    try:
                        first_move = await client.wait_for("message", check=lambda reply: reply.author.id in [message.author.id, opponent_id] and not reply.guild, timeout=120.0)
                        if first_move.author.id == message.author.id and first_move.content.upper() in author_hand:
                            await message.author.send(embed=create_embed(f"You have played: {first_move.content}"))
                            author_move = first_move
                            break
                        elif first_move.author.id == opponent_id and first_move.content.upper() in opponent_hand:
                            await opponent_author.send(embed=create_embed(f"You have played: {first_move.content}"))
                            opponent_move = first_move
                            break
                        else:
                            await first_move.author.send(embed=create_embed("Invalid move"))
                    except asyncio.TimeoutError:
                        return await message.channel.send(embed=create_embed(f'Sorry, the move took too long.'))
                    
                while not opponent_move:
                    try:
                        opponent_move = await client.wait_for("message", check=lambda reply: reply.author.id == opponent_id and not reply.guild, timeout=120.0)
                        if opponent_move.content.upper() in opponent_hand:
                            await opponent_author.send(embed=create_embed(f"You have played: {opponent_move.content}"))
                        else:
                            await opponent_author.send(embed=create_embed("Invalid move"))
                            opponent_move = ""
                    except asyncio.TimeoutError:
                        return await message.channel.send(embed=create_embed(f'Sorry, the move took too long.'))
                
                while not author_move:
                    try:
                        author_move = await client.wait_for("message", check=lambda reply: reply.author.id == message.author.id and not reply.guild, timeout=120.0)
                        if author_move.content.upper() in author_hand:
                            await message.author.send(embed=create_embed(f"You have played: {author_move.content}"))
                        else:
                            await message.author.send(embed=create_embed("Invalid move"))
                            author_move = ""
                    except asyncio.TimeoutError:
                        return await message.channel.send(embed=create_embed(f'Sorry, the move took too long.'))
                
                

                opponent_hand.remove(opponent_move.content)
                author_hand.remove(author_move.content)

                await message.author.send(embed=create_embed(f"You played a {author_move.content}\n{opponent_mention} played a {opponent_move.content}"))
                await opponent_author.send(embed=create_embed(f"You played a {opponent_move.content}\n{message.author.mention} played a {author_move.content}"))

                match opponent_move.content.upper():
                    case "A":
                        opponent_move = 1
                    case "J":
                        opponent_move = 11
                    case "Q":
                        opponent_move = 12
                    case "K":
                        opponent_move = 13
                    case _:
                        opponent_move = int(opponent_move.content)
                match author_move.content.upper():
                    case "A":
                        author_move = 1
                    case "J":
                        author_move = 11
                    case "Q":
                        author_move = 12
                    case "K":
                        author_move = 13
                    case _:
                        author_move = int(author_move.content)

                """
                await message.channel.send(f"{message.author.mention} played a {author_move}.\n{opponent_mention} played a {opponent_move}.")
                """
                
                if author_move > opponent_move:
                    """
                    await message.channel.send(f"{message.author.mention} wins the prize(s)!")
                    """
                    await message.author.send(embed=create_embed("You won the prize(s)!"))
                    await opponent_author.send(embed=create_embed("They won the prize(s)!"))
                    author_prizes.extend(upturned)
                    upturned = []
                elif opponent_move > author_move:
                    """
                    await message.channel.send(f"{opponent_mention} wins the prize(s)!")
                    """
                    await message.author.send(embed=create_embed("They won the prize(s)!"))
                    await opponent_author.send(embed=create_embed("You won the prize(s)!"))
                    opponent_prizes.extend(upturned)
                    upturned = []
                elif opponent_move == author_move:
                    """
                    await message.channel.send("It's a tie!")
                    """
                    await message.author.send(embed=create_embed("It's a tie!"))
                    await opponent_author.send(embed=create_embed("It's a tie!"))
                else:
                    await message.channel.send(embed=create_embed("I am in error help pls"))

            await message.author.send(embed=create_embed("The game has ended!"))
            await opponent_author.send(embed=create_embed("The game has ended!"))
            author_score = sum(author_prizes)
            opponent_score = sum(opponent_prizes)
            result = author_score - opponent_score
            await message.channel.send(embed=create_embed(f"{message.author.mention} final score: {author_score}\n{opponent_mention} final score: {opponent_score}"))
            if result > 0:
                await message.channel.send(embed=create_embed(f"{message.author.mention} wins the game by {result}!!!"))
            elif result < 0:
                result *= -1
                await message.channel.send(embed=create_embed(f"{opponent_mention} wins the game by {result}!!!"))
            else:
                await message.channel.send(embed=create_embed(f"Both players tied somehow!"))

client.run("MTE2NzE2NzM1NDk4MDAxNjIwMw.GphUqg.KmLq7KsnJTpv_pcDDTBqMXebGES-x1fopt7tS4")
