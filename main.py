import discord
import random
import asyncio

client = discord.Client(intents=discord.Intents.all())

def create_embed(desc, footer=None, colour=discord.Color.from_rgb(0, 0, 0)):
    embed = discord.Embed(
        colour=colour,
        description=f"**{desc}**",
        title="Game of Pure Strategy"
    )
    if footer:
        embed.set_footer(text=footer)
    return embed

def sum_cards(cards):
    result = 0
    for card in cards:
        if card == "A": 
            result += 1
        elif card == "J":
            result += 11
        elif card == "Q":
            result += 12
        elif card == "K":
            result += 13
        else:
            result += int(card)
    return result


def create_cards(cards, suit):
    message = ""

    if suit in ["diamonds", "hearts"]:
        suit_colour = "r"
    else:
        suit_colour = "b"

    if len(cards) > 10:
        first_pass = cards[:10]
        len_first_pass = 10
    else:
        first_pass = cards
        len_first_pass = len(cards)

    for card in first_pass:
        if suit_colour == "r":
            if card == "A":
                message += "<:rA:1167547696308027573>"
            elif card == "2":
                message += "<:r2:1167547670118813726>"
            elif card == "3":
                message += "<:r3:1167547671620358175>"
            elif card == "4":
                message += "<:r4:1167547674065649786>"
            elif card == "5":
                message += "<:r5:1167547661075894293>"
            elif card == "6":
                message += "<:r6:1167547664435523674>"
            elif card == "7":
                message += "<:r7:1167547665878368267>"
            elif card == "8":
                message += "<:r8:1167547668323631247>"
            elif card == "9":
                message += "<:r9:1167547707972395018>"
            elif card == "10":
                message += "<:r10:1167547709675286639>"
            elif card == "J":
                message += "<:rJ:1167547700154212402>"
            elif card == "Q":
                message += "<:rQ:1167547704168169607>"
            elif card == "K":
                message += "<:rK:1167547701488009287>"

        if suit_colour == "b":
            if card == "A":
                message += "<:bA:1167547616259747900>"
            elif card == "2":
                message += "<:b2:1167547529513160824>"
            elif card == "3":
                message += "<:b3:1167547552535691304>"
            elif card == "4":
                message += "<:b4:1167547554515402884>"
            elif card == "5":
                message += "<:b5:1167547556121804920>"
            elif card == "6":
                message += "<:b6:1167547559129137323>"
            elif card == "7":
                message += "<:b7:1167547561935126629>"
            elif card == "8":
                message += "<:b8:1167547564447502456>"
            elif card == "9":
                message += "<:b9:1167547565848416440>"
            elif card == "10":
                message += "<:b10:1167547581140840470>"
            elif card == "J":
                message += "<:bJ:1167547607732723762>"
            elif card == "Q":
                message += "<:bQ:1167546141294993498>"
            elif card == "K":
                message += "<:bK:1167547608974233640>"
            

    if cards:
        message += "\n"

    if suit == "diamonds":
        message += "<:ediamonds:1167547698711379988>"*len_first_pass
    elif suit == "hearts":
        message += "<:ehearts:1167547614837870592>"*len_first_pass
    elif suit == "clubs":
        message += "<:eclubs:1167547612493262929>"*len_first_pass
    elif suit == "spades":
        message += "<:espades:1167547715270492382>"*len_first_pass

    if len_first_pass != 10:
        return message
    
    message += "\n"
    second_pass = create_cards(cards[10:], suit)
    message += second_pass

    return message

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$gops '):
            if len(message.content) < 7:
                if message.content[6] == " ":
                    return
            opponent_id = int(message.content[8:-1])
            opponent_author = client.get_user(opponent_id)
            opponent_mention = message.content[6:-1] + ">"
            opponent_display_name = opponent_author.display_name
            author_display_name = message.author.display_name

            offer = await message.channel.send(embed=create_embed(f"{message.author.mention} wants to play a game of GOPS with you, {opponent_mention}.\nDo you accept?"))
            await offer.add_reaction("🇾")
            await offer.add_reaction("🇳")

            

            try:
                opponent_reaction = await client.wait_for("reaction_add", check=lambda reaction, user: reaction.emoji in ["🇾", "🇳"] and user.id == opponent_id, timeout=60.0)
            except asyncio.TimeoutError:
                 return await message.channel.send(embed=create_embed(f'Sorry, {opponent_mention} took too long to respond.'))

            opponent_emoji = opponent_reaction[0].emoji
            if opponent_emoji == "🇾":
                 await message.channel.send(embed=create_embed(f"{message.author.mention}, {opponent_mention} The game is starting!"))
            elif opponent_emoji == "🇳":
                 return await message.channel.send(embed=create_embed("Game offer declined."))

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

            suits = ["diamonds", "hearts", "clubs", "spades"]
            
            """
            suit_choice = await message.channel.send(embed=create_embed(f"{message.author.mention} wants to play a game of GOPS with you, {opponent_mention}.\nDo you accept?"))
            await offer.add_reaction("🇾")
            await offer.add_reaction("🇳")
            try:
                opponent_reaction = await client.wait_for("reaction_add", check=lambda reaction, user: reaction.emoji in ["🇾", "🇳"] and user.id == opponent_id, timeout=60.0)
            except asyncio.TimeoutError:
                 return await message.channel.send(embed=create_embed(f'Sorry, {opponent_mention} took too long to respond.'))
            """

            opponent_emoji = opponent_reaction[0].emoji
            if opponent_emoji == "🇾":
                 await message.channel.send(embed=create_embed(f"{message.author.mention}, {opponent_mention} The game is starting!"))
            elif opponent_emoji == "🇳":
                 return await message.channel.send(embed=create_embed("Game offer declined."))

            author_suit = suits.pop()
            opponent_suit = suits.pop()
            stock_suit = suits.pop()

            for i in range(13):
                upturned.append(stock.pop())
                cards_remaining = len(stock)-1
                author_move, opponent_move = "", ""

                upturned_display = create_cards(upturned, stock_suit)
                author_hand_display = create_cards(author_hand, author_suit)
                opponent_hand_display = create_cards(opponent_hand, opponent_suit)
                author_prizes_display = create_cards(author_prizes, stock_suit)
                opponent_prizes_display = create_cards(opponent_prizes, stock_suit)

                author_prize_total = sum_cards(author_prizes)
                opponent_prize_total = sum_cards(opponent_prizes)
                upturned_prize_total = sum_cards(upturned)

                await message.author.send(embed=create_embed(f"Upturned({upturned_prize_total}):\n{upturned_display}\nYour hand:\n{author_hand_display}\nYour prizes({author_prize_total}):\n{author_prizes_display}\n{opponent_display_name}'s prizes({opponent_prize_total}):\n{opponent_prizes_display}", f"Cards remaining in deck: {cards_remaining}"))
                await opponent_author.send(embed=create_embed(f"Upturned({upturned_prize_total}):\n{upturned_display}\nYour hand:\n{opponent_hand_display}\nYour prizes({opponent_prize_total}):\n{opponent_prizes_display}\n{author_display_name}'s prizes({author_prize_total}):\n{author_prizes_display}", f"Cards remaining in deck: {cards_remaining}"))

                while not opponent_move or not author_move:
                    try:
                        first_move = await client.wait_for("message", check=lambda reply: reply.author.id in [message.author.id, opponent_id] and not reply.guild, timeout=120.0)
                        print(first_move.content)
                        if first_move.author.id == message.author.id and first_move.content.upper() in author_hand:
                            await message.author.send(embed=create_embed(f"Waiting on opponent..."))
                            author_move = first_move
                            break
                        elif first_move.content.startswith("$send "):
                            if first_move.author.id == message.author.id:
                                await opponent_author.send(embed=create_embed(f"{author_display_name} sent a message:\n{first_move.content[6:]}"))
                            else:
                                await message.author.send(embed=create_embed(f"{opponent_display_name} sent a message:\n{first_move.content[6:]}"))
                        elif first_move.author.id == opponent_id and first_move.content.upper() in opponent_hand:
                            await opponent_author.send(embed=create_embed(f"Waiting on opponent..."))
                            opponent_move = first_move
                            break
                        else:
                            await first_move.author.send(embed=create_embed("Invalid move"))
                    except asyncio.TimeoutError:
                        return await message.channel.send(embed=create_embed(f'Sorry, the move took too long.'))
                    
                while not opponent_move:
                    print("o")
                    try:
                        opponent_move = await client.wait_for("message", check=lambda reply: reply.author.id in [opponent_id, message.author.id] and not reply.guild, timeout=120.0)
                        if opponent_move.content.startswith("$send "):
                            if opponent_move.author.id == message.author.id:
                                await opponent_author.send(embed=create_embed(f"{author_display_name} sent a message:\n{opponent_move.content[6:]}"))
                            else:
                                await message.author.send(embed=create_embed(f"{opponent_display_name} sent a message:\n{opponent_move.content[6:]}"))
                            opponent_move = ""
                        elif not opponent_move.content.upper() in opponent_hand:
                            await opponent_author.send(embed=create_embed("Invalid move"))
                            opponent_move = ""
                        elif not opponent_move.author.id == opponent_id:
                            opponent_move = ""
                    except asyncio.TimeoutError:
                        return await message.channel.send(embed=create_embed(f'Sorry, the move took too long.'))
                
                while not author_move:
                    try:
                        author_move = await client.wait_for("message", check=lambda reply: reply.author.id in [opponent_id, message.author.id] and not reply.guild, timeout=120.0)
                        if author_move.content.startswith("$send "):
                            if author_move.author.id == message.author.id:
                                await opponent_author.send(embed=create_embed(f"{author_display_name} sent a message:\n{author_move.content[6:]}"))
                            else:
                                await message.author.send(embed=create_embed(f"{opponent_display_name} sent a message:\n{author_move.content[6:]}"))
                            author_move = ""
                        elif not author_move.content.upper() in author_hand:
                            await message.author.send(embed=create_embed("Invalid move"))
                            author_move = ""
                        elif not author_move.author.id == message.author.id:
                            author_move = ""
                    except asyncio.TimeoutError:
                        return await message.channel.send(embed=create_embed(f'Sorry, the move took too long.'))
                
                

                opponent_hand.remove(opponent_move.content.upper())
                author_hand.remove(author_move.content.upper())

                author_move_display = create_cards([author_move.content], author_suit)
                opponent_move_display = create_cards([opponent_move.content], opponent_suit)
                author_move_display, opponent_move_display = f"You played:\n{author_move_display}\n{opponent_display_name} played:\n{opponent_move_display}", f"You played:\n{opponent_move_display}\n{author_display_name} played:\n{author_move_display}"

                if opponent_move.content.upper() == "A":
                    opponent_move = 1
                elif opponent_move.content.upper() == "J":
                    opponent_move = 11
                elif opponent_move.content.upper() == "Q":
                    opponent_move = 12
                elif opponent_move.content.upper() == "K":
                    opponent_move = 13
                else:
                    opponent_move = int(opponent_move.content)

                if author_move.content.upper() == "A":
                    author_move = 1
                elif author_move.content.upper() == "J":
                    author_move = 11
                elif author_move.content.upper() == "Q":
                    author_move = 12
                elif author_move.content.upper() == "K":
                    author_move = 13
                else:
                    author_move = int(author_move.content)
                
                if author_move > opponent_move:
                    author_move_display += "\nYou won the prize(s)!"
                    opponent_move_display += "\nThey won the prize(s)."
                    author_colour = discord.Color.from_rgb(22, 100, 8)
                    opponent_colour = discord.Color.from_rgb(255, 49, 49)
                    author_prizes.extend(upturned)
                    upturned = []
                elif opponent_move > author_move:
                    author_move_display += "\nThey won the prize(s)!"
                    opponent_move_display += "\nYou won the prize(s)!"
                    author_colour = discord.Color.from_rgb(255, 49, 49)
                    opponent_colour = discord.Color.from_rgb(255, 49, 49)
                    opponent_prizes.extend(upturned)
                    upturned = []
                elif opponent_move == author_move:
                    author_move_display += "\nIt's a tie!"
                    opponent_move_display += "\nIt's a tie!"
                    author_colour = discord.Color.from_rgb(224, 231, 34)
                    opponent_colour = discord.Color.from_rgb(224, 231, 34)
                else:
                    await message.channel.send(embed=create_embed("I am in error help pls"))
                
                await message.author.send(embed=create_embed(author_move_display, colour=author_colour))
                await opponent_author.send(embed=create_embed(opponent_move_display, colour=opponent_colour))


            await message.author.send(embed=create_embed("The game has ended!"))
            await opponent_author.send(embed=create_embed("The game has ended!"))
            author_score = sum_cards(author_prizes)
            opponent_score = sum_cards(opponent_prizes)
            result = author_score - opponent_score
            await message.channel.send(embed=create_embed(f"Final Scores:\n{message.author.mention}: {author_score}\n{opponent_mention}: {opponent_score}"))
            if result > 0:
                return await message.channel.send(embed=create_embed(f"🎉{message.author.mention} won the game by {result}!🎉"))
            elif result < 0:
                result *= -1
                return await message.channel.send(embed=create_embed(f"🎉{opponent_mention} won the game by {result}!🎉"))
            else:
                return await message.channel.send(embed=create_embed(f"{message.author.mention} and {opponent_mention} tied somehow!"))
    elif message.content == '$mowareking':
        return await message.channel.send(embed=create_embed("My Creator"))
    elif message.content == "$help":
        pass



client.run("MTE2NzE2NzM1NDk4MDAxNjIwMw.GphUqg.KmLq7KsnJTpv_pcDDTBqMXebGES-x1fopt7tS4")
