import discord
import random
import asyncio
import os
import json
import csv
#from keep_alive import keep_alive
from key import TOKEN

client = discord.Client(intents=discord.Intents.all())
users_playing = []

with open("stats.json") as f:
    users_stats = json.load(f)

class User():
    def __init__(self, id, suit):
        self.id = id
        self.author = client.get_user(self.id)
        self.mention = self.author.mention
        self.display_name = self.author.display_name.capitalize()
        self.suit = suit
        self.hand = create_suit()
        self.hand_display = create_cards(self.hand, self.suit)
        self.prizes = []
        self.prizes_display = ""
        self.prizes_total = 0
        self.move = None
        self.move_display = ""
        self.colour = None

    async def send_current_move(self, upturned, upturned_display, upturned_total, cards_remaining, other_player):
        await self.author.send(embed=create_embed(f"Upturned({upturned_total}):\n{upturned_display}\nYour hand:\n{self.hand_display}\nYour prizes({self.prizes_total}):\n{self.prizes_display}\n{other_player.display_name}'s prizes({other_player.prizes_total}):\n{other_player.prizes_display}", f"Cards remaining in deck: {cards_remaining}"))

    async def await_move(self, other_player, channel, timeout):
        while not self.move:
            second_move = await client.wait_for("message", check=lambda reply: reply.author.id in [other_player.id, self.author.id] and not reply.guild, timeout=timeout)
            if second_move.content.startswith("$send "):
                if second_move.author.id == self.author.id:
                    await other_player.author.send(embed=create_embed(f"{self.display_name} sent a message:\n{second_move.content[6:]}"))
                    await self.author.send(embed=create_embed(f"Message has been sent."))
                else:
                    await self.author.send(embed=create_embed(f"{other_player.display_name} sent a message:\n{second_move.content[6:]}"))
                    await other_player.author.send(embed=create_embed(f"Message has been sent."))
            elif second_move.content == "$forfeit":
                if second_move.author.id == self.id:
                    await self.author.send(embed=create_embed(f"You have forfeited the game."))
                    await other_player.author.send(embed=create_embed(f"{self.display_name} forfeited the game."))
                    return self.id
                else:
                    await other_player.author.send(embed=create_embed(f"You have forfeited the game."))
                    await self.author.send(embed=create_embed(f"{other_player.display_name} forfeited the game."))
                    return other_player.id
            elif not second_move.content.upper() in self.hand:
                if second_move.author.id == self.id:
                    await second_move.author.send(embed=create_embed("Invalid move."))
            elif second_move.author.id == self.id:
                self.move = second_move.content.upper()


    def execute_move(self):
        self.hand.remove(self.move)
        self.hand_display = create_cards(self.hand, self.suit)
        self.move_display = create_cards([self.move], self.suit)
        self.match_move()

    def match_move(self):
        if self.move == "A":
            self.move = 1
        elif self.move == "J":
            self.move = 11
        elif self.move == "Q":
            self.move = 12
        elif self.move == "K":
            self.move = 13
        else:
            self.move = int(self.move)

    async def send_result(self, other_player, prizes_won=False, tie=False, suit="diamonds"):
        message = f"You played:\n{self.move_display}\n{other_player.display_name} played:\n{other_player.move_display}"
        if prizes_won:
            message += "\nYou won the prize(s)!"
            self.colour = discord.Color.from_rgb(22, 100, 8)
            self.prizes.extend(prizes_won)
            self.prizes_display = create_cards(self.prizes, suit)
            self.prizes_total = sum_cards(self.prizes)
        elif tie:
            message += "\nIt's a tie!"
            self.colour = discord.Color.from_rgb(224, 231, 34)
        else:
            message += "\nThey won the prize(s)!"
            self.colour = discord.Color.from_rgb(255, 49, 49)
        await self.author.send(embed=create_embed(message, colour=self.colour))


def create_suit():
    royals = ["J", "Q", "K"]
    suit = [str(x) for x in range(2, 11)]
    suit.insert(0, "A")
    suit.extend(royals)
    return suit


def create_embed(desc, footer=None, title="Game of Pure Strategy", colour=discord.Color.from_rgb(0, 0, 0), bold=True):
    if bold:
        desc = f"**{desc}**"
    embed = discord.Embed(
        colour=colour,
        description=desc,
        title=title
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
                message += "<:rA:1169599443759272047>"
            elif card == "2":
                message += "<:r2:1169599490429304852>"
            elif card == "3":
                message += "<:r3:1169599492673241150>"
            elif card == "4":
                message += "<:r4:1169599494963331072>"
            elif card == "5":
                message += "<:r5:1169599514785620068>"
            elif card == "6":
                message += "<:r6:1169599517994262559>"
            elif card == "7":
                message += "<:r7:1169599600643018842>"
            elif card == "8":
                message += "<:r8:1169599602899558440>"
            elif card == "9":
                message += "<:r9:1169599440072486942>"
            elif card == "10":
                message += "<:r10:1169599442391937064>"
            elif card == "J":
                message += "<:rJ:1169599461379551263>"
            elif card == "Q":
                message += "<:rQ:1169599598298398760>"
            elif card == "K":
                message += "<:rK:1169599605466472580>"

        if suit_colour == "b":
            if card == "A":
                message += "<:bA:1169599215425556590>"
            elif card == "2":
                message += "<:b2:1169599236237692948>"
            elif card == "3":
                message += "<:b3:1169599242910847046>"
            elif card == "4":
                message += "<:b4:1169599247289683979>"
            elif card == "5":
                message += "<:b5:1169599254860402728>"
            elif card == "6":
                message += "<:b6:1169599265614602271>"
            elif card == "7":
                message += "<:b7:1169599283138408548>"
            elif card == "8":
                message += "<:b8:1169599209037639831>"
            elif card == "9":
                message += "<:b9:1169599212011405312>"
            elif card == "10":
                message += "<:b10:1169599213412302878>"
            elif card == "J":
                message += "<:bJ:1169599217686286376>"
            elif card == "Q":
                message += "<:bQ:1169599230487302144>"
            elif card == "K":
                message += "<:bK:1169599226372685925>"


    if cards:
        message += "\n"

    if suit == "diamonds":
        message += "<:ediamond:1169599445285998673>"*len_first_pass
    elif suit == "hearts":
        message += "<:ehearts:1169599296602120193>"*len_first_pass
    elif suit == "clubs":
        message += "<:eclubs:1169599234190880818>"*len_first_pass
    elif suit == "spades":
        message += "<:espades:1169599488487325738>"*len_first_pass

    if len_first_pass != 10:
        return message

    message += "\n"
    second_pass = create_cards(cards[10:], suit)
    message += second_pass
    return message

def generate_data(move, computer_hand, opponent_hand, upturned_total, stock):
  if move == "A":
      move = 1
  elif move == "J":
      move = 11
  elif move == "Q":
      move = 12
  elif move == "K":
      move = 13
  else:
      move = int(move)
  data = [move]
  for cards in [computer_hand, opponent_hand, stock]:
      if "A" in cards:
          data.append(1)
      else:
          data.append(0)
      for i in range(2, 11):
          if str(i) in cards:
              data.append(1)
          else:
              data.append(0)
      for royal in ["J", "Q", "K"]:
          if royal in cards:
              data.append(1)
          else:
              data.append(0)
  data.append(int(upturned_total))
  return data

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.guild:
        return
    if message.content.startswith("$play "):
        suits = ["diamonds", "hearts", "clubs", "spades"]
        random.shuffle(suits)

        player = User(message.author.id, suits.pop())
        try:
            opponent = User(int(message.content[8:-1]), suits.pop())
        except (ValueError, AttributeError):
            return await message.channel.send(embed=create_embed("Invalid user mention"))

        if opponent.id == player.id:
            return await message.channel.send(embed=create_embed("Hey, you can't play against yourself silly!"))
        if opponent.id == client.user.id:
            return await message.channel.send(embed=create_embed("I'm flattered but unfortunately my creator hasn't given me a brain, at least not yet."))
        if player.id in users_playing:
            return await message.channel.send(embed=create_embed("You are in a game!"))
        if opponent.id in users_playing:
            return await message.channel.send(embed=create_embed(f"{opponent.mention} is in a game!"))
        
        offer = await message.channel.send(embed=create_embed(f"{player.mention} wants to play a game of GOPS with you, {opponent.mention}.\nDo you accept?"))
        await offer.add_reaction("🇾")
        await offer.add_reaction("🇳")

        try:
            opponent_reaction = await client.wait_for("reaction_add", check=lambda reaction, user: reaction.emoji in ["🇾", "🇳"] and user.id == opponent.id, timeout=60.0)
        except asyncio.TimeoutError:
            return await message.channel.send(embed=create_embed(f'Sorry, {opponent.mention} took too long to respond.'))

        opponent_emoji = opponent_reaction[0].emoji

        if opponent_emoji == "🇳":
                return await message.channel.send(embed=create_embed(f"{opponent.mention} declined game offer."))
        await message.channel.send(embed=create_embed(f"{player.mention}, {opponent.mention} The game is starting!"))

        users_playing.append(opponent.id)
        users_playing.append(player.id)

        if not str(opponent.id) in users_stats.keys():
            users_stats[str(opponent.id)] = [0, 0, 0]
            with open('stats.json', 'w') as f:
                stats = json.dumps(users_stats, indent=4)
                print(stats, file=f)
        if not str(player.id) in users_stats.keys():
            users_stats[str(player.id)] = [0, 0, 0]
            with open('stats.json', 'w') as f:
                stats = json.dumps(users_stats, indent=4)
                print(stats, file=f)

        upturned = []
        stock = create_suit()
        random.shuffle(stock)
        stock_suit = suits.pop() 
        timeout = 180.0
        log_channel = client.get_channel(1168995474255130774)

        for i in range(13):
            upturned.append(stock.pop())
            upturned_display = create_cards(upturned, stock_suit)
            upturned_total = sum_cards(upturned)
            cards_remaining = len(stock)
            opponent.move = None
            player.move = None

            await player.send_current_move(upturned, upturned_display, upturned_total, cards_remaining, opponent)
            await opponent.send_current_move(upturned, upturned_display, upturned_total, cards_remaining, player)

            while not opponent.move and not player.move:
                try:
                    first_move = await client.wait_for("message", check=lambda reply: reply.author.id in [player.id, opponent.id] and not reply.guild, timeout=timeout)
                    if first_move.content.startswith("$send "):
                        if first_move.author.id == player.id:
                            await opponent.author.send(embed=create_embed(f"{player.display_name} sent a message:\n{first_move.content[6:]}"))
                            await player.author.send(embed=create_embed(f"Message has been sent."))
                        else:
                            await player.author.send(embed=create_embed(f"{opponent.display_name} sent a message:\n{first_move.content[6:]}"))
                            await opponent.author.send(embed=create_embed(f"Message has been sent."))
                    elif first_move.content == "$forfeit":
                        if first_move.author.id == player.id:
                            await player.author.send(embed=create_embed(f"You have forfeited the game."))
                            await opponent.author.send(embed=create_embed(f"{player.display_name} forfeited the game."))
                            users_playing.remove(player.id)
                            users_playing.remove(opponent.id)
                            return await message.channel.send(embed=create_embed(f"{player.mention} forfeited the game."))
                        else:
                            await opponent.author.send(embed=create_embed(f"You have forfeited the game."))
                            await player.author.send(embed=create_embed(f"{opponent.display_name} forfeited the game."))
                            users_playing.remove(player.id)
                            users_playing.remove(opponent.id)
                            return await message.channel.send(embed=create_embed(f"{opponent.mention} forfeited the game."))
                    elif first_move.author.id == player.id and first_move.content.upper() in player.hand:
                        await player.author.send(embed=create_embed(f"Waiting for opponent..."))
                        player.move = first_move.content.upper()
                    elif first_move.author.id == opponent.id and first_move.content.upper() in opponent.hand:
                        await opponent.author.send(embed=create_embed(f"Waiting for opponent..."))
                        opponent.move = first_move.content.upper()
                    else:
                        await first_move.author.send(embed=create_embed("Invalid move."))
                except asyncio.TimeoutError:
                    users_playing.remove(player.id)
                    users_playing.remove(opponent.id)
                    return await message.channel.send(embed=create_embed(f'Sorry, the move took too long.'))

            if not opponent.move:
                try:
                    forfeited = await opponent.await_move(player, message.channel, timeout)
                    if forfeited == player.id:
                        users_playing.remove(player.id)
                        users_playing.remove(opponent.id)
                        return await message.channel.send(embed=create_embed(f"{player.mention} forfeited the game."))
                    elif forfeited == opponent.id:
                        users_playing.remove(player.id)
                        users_playing.remove(opponent.id)
                        return await message.channel.send(embed=create_embed(f"{opponent.mention} forfeited the game."))
                except asyncio.TimeoutError:
                    users_playing.remove(player.id)
                    users_playing.remove(opponent.id)
                    return await message.channel.send(embed=create_embed(f'Sorry, the move took too long.'))
            else:
                try:
                    forfeited = await player.await_move(opponent, message.channel, timeout)
                    if forfeited == player.id:
                        users_playing.remove(player.id)
                        users_playing.remove(opponent.id)
                        return await message.channel.send(embed=create_embed(f"{player.mention} forfeited the game."))
                    elif forfeited == opponent.id:
                        users_playing.remove(player.id)
                        users_playing.remove(opponent.id)
                        return await message.channel.send(embed=create_embed(f"{opponent.mention} forfeited the game."))
                except asyncio.TimeoutError:
                    users_playing.remove(player.id)
                    users_playing.remove(opponent.id)
                    return await message.channel.send(embed=create_embed(f'Sorry, the move took too long.'))

            moves_data = open("training_data.csv", "a", newline="")
            opponent_data = generate_data(opponent.move, player.hand, opponent.hand, upturned_total, stock)
            player_data = generate_data(player.move, opponent.hand, player.hand, upturned_total, stock)
            writer = csv.writer(moves_data)
            writer.writerow(opponent_data)
            writer.writerow(player_data) 
            moves_data.close()

            opponent.execute_move()
            player.execute_move()

            await log_channel.send(embed=create_embed(f"Upturned({upturned_total}):\n{upturned_display}\n{player.display_name} played:\n{player.move_display}\n{opponent.display_name} played:\n{opponent.move_display}\n{player.display_name} prizes({player.prizes_total}):\n{player.prizes_display}\n{opponent.display_name} prizes({opponent.prizes_total}):\n{opponent.prizes_display}", title=f"{player.display_name} v {opponent.display_name}"))

            if player.move > opponent.move:
                await player.send_result(opponent, upturned, suit=stock_suit)
                await opponent.send_result(player, suit=stock_suit)
                upturned = []
            elif opponent.move > player.move:
                await player.send_result(opponent, suit=stock_suit)
                await opponent.send_result(player, upturned, suit=stock_suit)
                upturned = []
            elif player.move == opponent.move:
                await player.send_result(opponent, tie=True, suit=stock_suit)
                await opponent.send_result(player, tie=True, suit=stock_suit)
            else:
                await message.channel.send(embed=create_embed("I am in error help pls"))


        await player.author.send(embed=create_embed("The game has ended!"))
        await opponent.author.send(embed=create_embed("The game has ended"))

        result = player.prizes_total - opponent.prizes_total

        users_playing.remove(player.id)
        users_playing.remove(opponent.id)

        await message.channel.send(embed=create_embed(f"Final Scores:\n{player.mention}: {player.prizes_total}\n{opponent.mention}: {opponent.prizes_total}"))
        if result > 0:
            users_stats[str(player.id)][0] += 1
            users_stats[str(opponent.id)][2] += 1
            with open('stats.json', 'w') as f:
                stats = json.dumps(users_stats, indent=4)
                print(stats, file=f)
            return await message.channel.send(embed=create_embed(f"🎉{player.mention} won against {opponent.mention} by {result} points!🎉"))
        elif result < 0:
            users_stats[str(opponent.id)][0] += 1
            users_stats[str(player.id)][2] += 1
            result *= -1
            with open('stats.json', 'w') as f:
                stats = json.dumps(users_stats, indent=4)
                print(stats, file=f)
            return await message.channel.send(embed=create_embed(f"🎉{opponent.mention} won against {player.mention} by {result} points!🎉"))
        else:
            users_stats[str(opponent.id)][1] += 1
            users_stats[str(player.id)][1] += 1
            with open('stats.json', 'w') as f:
                stats = json.dumps(users_stats, indent=4)
                print(stats, file=f)
            return await message.channel.send(embed=create_embed(f"{player.mention} and {opponent.mention} tied somehow!"))

    elif message.content == '$mowareking':
        return await message.channel.send(embed=create_embed("My Creator"))
    elif message.content == "$rules" or message.content.startswith("$rules "):
        rules = "**The Game of Pure Strategy (a.k.a GOPS) is a two-played purely strategical playing card game.**\n\n**Deck and Hands**\nEach player starts with one suit of cards in their hand. One suit is discarded and the other suit is shuffled and forms the draw deck.\n\n**Points**\nThe Ace is worth 1 point, the face cards are worth their face values, and the Jack, Queen, and King are worth 11, 12, and 13 points, respectively.\n\n**Gameplay**\nThe top card of the draw deck is placed face down. Players then place one card face down as a bid and simultaneously flip them. The player with the higher-ranking bid wins the upturned prize card. Both bids are then discarded, and a new card is drawn. The process repeats until the draw deck and hands are exhausted. In the event of a tie, both bids are discarded, and another prize card is drawn, and players now bid for all the prize cards.\n\n**Winner**\nThe winner is the player who's prize cards total is largest."
        return await message.channel.send(embed=create_embed(rules, title="How to play: The Game of Pure Strategy", bold=False))
    elif message.content == "$help" or message.content.startswith("$help "):
        commands = "$play (user) - Starts a GOPS game between you and the mentioned player\n$rules - Shows the rules of the playing card game GOPS\n$help - Shows all the commands for this bot\n$send (message) - Send messages to your opponent during a game\n$forfeit - Forfeits the game\n$stats - Shows your W/D/L ratio\n$leaderboard - Shows the W/D/L ratio of every player"
        return await message.channel.send(embed=create_embed(commands, title="Commands"))  
    elif message.content == "$send" or message.content.startswith("$send "):
        return await message.channel.send(embed=create_embed("Use this during a game to send a message to your opponent!")) 
    elif message.content == "$stats" or message.content.startswith("$stats "):
        id = str(message.author.id)
        if not id in users_stats.keys():
            users_stats[id] = [0, 0, 0]
            with open('stats.json', 'w') as f:
                stats = json.dumps(users_stats, indent=4)
                print(stats, file=f)
        user_stats = users_stats[id]
        return await message.channel.send(embed=create_embed(f"W/D/L:  {user_stats[0]}/{user_stats[1]}/{user_stats[2]}", title="Stats"))
    elif message.content == "$leaderboard" or message.content.startswith("$leaderboard "):
        msg = ""
        for player, stats in users_stats.items():
            player = client.get_user(int(player))
            msg += f"{player.display_name}: {stats[0]}/{stats[1]}/{stats[2]}\n)"
        msg = msg[:-2].replace(")", "")
        return await message.channel.send(embed=create_embed(msg, title="Leaderboard", bold=False))



#keep_alive()
client.run(TOKEN)