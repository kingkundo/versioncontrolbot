# bot.py
# Tom Taylor / Version Control
# 2021

import os
from gil import get_currency_str
from twitchio.ext import commands
from random import randint
from glob import glob
from playsound import playsound
from threading import Thread
from time import time
from chatuser import save_backup as save_users_backup, populate_user_data_cache, get_user_currency, add_user_currency, spend_user_currency

# GLOBALS -----------------------------
MINIMUM_SECS_BETWEEN_SFX = 20
MINIMUM_SECS_BETWEEN_PAYOUTS = 900
AMOUNT_TO_PAY_OUT_REGULARLY = 100
STREAMER_INFO = None

# CONFIG ------------------------------

bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']],
    client_secret=os.environ['CLIENT_SECRET']
)

# HELPERS ----------------------------

async def does_user_follow_streamer(follower_user_id : int) -> bool:
    if follower_user_id == int(STREAMER_INFO.id):
        return True

    user_follows_streamer = await bot.get_follow(follower_user_id, STREAMER_INFO.id)
    return (user_follows_streamer is not None) and ('followed_at' in user_follows_streamer) and (user_follows_streamer['followed_at'] != '')

async def give_all_chat_users_gil(amount : int):
    chat_users = await bot.get_chatters(os.environ['CHANNEL'])
    for user in chat_users.all:
        add_user_currency(user, amount)
        print(f'{user} has been paid {amount} for tuning in')

# EVENTS ------------------------------

# EVENT - ON BOT ENTERING CHAT
@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    global STREAMER_INFO
    STREAMER_INFO = await bot.get_users(os.environ['CHANNEL'])
    STREAMER_INFO = STREAMER_INFO[0]

    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has arrived! 🎉")

# EVENT - ON MESSAGE IN CHAT
last_payout_time = time()
@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
        return

    await bot.handle_commands(ctx)

    # Handle custom commands...

    if 'hello bot' in ctx.content.lower():
        await ctx.channel.send(f"Hey, @{ctx.author.name} ❤️")

    # If the stream is live, and people have been in chat for X mins, then they get a payout
    global last_payout_time
    secs_since_last_payout = (time() - last_payout_time)
    if (secs_since_last_payout > MINIMUM_SECS_BETWEEN_PAYOUTS) and (await bot.get_stream(os.environ['CHANNEL']) is not None):
        await give_all_chat_users_gil(AMOUNT_TO_PAY_OUT_REGULARLY)
        last_payout_time = time()

# COMMANDS ------------------------------

# COMMAND - GET HELP ON HOW THE STREAM STUFF WORKS
@bot.command(name='help')
async def help(ctx):
    await ctx.send(f"@{ctx.author.name} {os.environ['HELP_STR']}")

# COMMAND - GET USERS CURRENCY
@bot.command(name='balance')
async def balance(ctx):
    await ctx.send(f'@{ctx.author.name} You have {get_user_currency(ctx.author.name)} in the bank 💰')

# COMMAND - ADD MORE CURRENCY TO A USER
@bot.command(name='addgil')
async def addgil(ctx):
    if not ctx.author.is_mod:
        await ctx.send(f'@{ctx.author.name} You must be a mod to perform this action 🛑')
        return

    components = ctx.content.split()

    if (len(components) == 3) and (components[2].isnumeric()):
        if components[1] == 'all':
            result = await give_all_chat_users_gil(int(components[2]))
            result_str = f'Everyone in chat has been given {get_currency_str(int(components[2]))} 🎉'
        else:
            result = add_user_currency(components[1], int(components[2]))
            result_str = f"{components[1]} has added {int(components[2])} to their original balance of {result['old']} and now has {result['new']}"
        print(result_str)
        await ctx.send(result_str)

# COMMAND - SPEND CURRENCY FROM A USER
@bot.command(name='spendgil')
async def spendgil(ctx):
    if not ctx.author.is_mod:
        await ctx.send(f'@{ctx.author.name} You must be a mod to perform this action 🛑')
        return

    components = ctx.content.split()

    if (len(components) == 3) and (components[2].isnumeric()):
        result = spend_user_currency(components[1], int(components[2]))
        result_str = f"{components[1]} has spent {int(components[2])} from their original balance of {result['old']} and now has {result['new']}"
        print(result_str)
        await ctx.send(result_str)

# COMMAND - GAMBLE
@bot.command(name='gamble')
async def gamble(ctx):
    if not await does_user_follow_streamer(ctx.author.id):
        await ctx.send(f'@{ctx.author.name} You must be a follower of the stream to perform this action 🛑')
        return

    components = ctx.content.split()

    if (len(components) < 2) or (not components[1].isnumeric()):
        await ctx.send(f'@{ctx.author.name} That value cannot be gambled with 🤪')
        return

    gamble_amount = int(components[1])
    users_balance = get_user_currency(ctx.author.name, False)
    if gamble_amount > users_balance:
        await ctx.send(f'@{ctx.author.name} You cannot gamble more than your balance 🤪')
        return

    potential_winnings = gamble_amount * 1.5
    dice_roll = randint(1,10)
    if dice_roll > 5:
        result = add_user_currency(ctx.author.name, potential_winnings)
        result_str = f"@{ctx.author.name} won the gamble! 🎉 They will receive 1.5x their gamble, bringing their balance from {users_balance} to {result['new']}"
        await ctx.send(result_str)
    else:
        result = spend_user_currency(ctx.author.name, gamble_amount)
        result_str = f"@{ctx.author.name} lost the gamble! 😭 Their balance has gone from {users_balance} to {result['new']}"
        await ctx.send(result_str)

    print(result_str)

    
# COMMAND - VIEW SFX LIST
@bot.command(name='sfxlist')
async def sfxlist(ctx):
    await ctx.send(os.environ['SFX_HELP_STR'])

# COMMAND - PLAY SFX
last_sfx_time = time()
@bot.command(name='sfx')
async def sfx(ctx):
    if not await does_user_follow_streamer(ctx.author.id):
        await ctx.send(f'@{ctx.author.name} You must be a follower of the stream to perform this action 🛑')
        return

    music_file_extension = '.mp3'
    sfxname = ctx.content.partition('sfx ')[2]
    sfxpath = f'{os.getcwd()}\sfx\{sfxname}*[0-9]*{music_file_extension}'
    fullsfxpath = ''
    gil_cost = 0
    for file in glob(sfxpath):
        fullsfxpath = file
        gil_cost = int(fullsfxpath[fullsfxpath.find(sfxname)+len(sfxname):fullsfxpath.rfind(music_file_extension)])

    if (sfxname == '') or (fullsfxpath == '') or (not os.path.exists(fullsfxpath)):
        await ctx.send(f'@{ctx.author.name} That sfx is invalid 😢')
        return

    user_balance = get_user_currency(ctx.author.name, False)
    if gil_cost > user_balance:
        await ctx.send(f"@{ctx.author.name} You don't have the gil balance to use this sfx. Your balance is {user_balance} and this sfx costs {gil_cost}")
        return

    global last_sfx_time

    secs_since_last_sfx = (time() - last_sfx_time)
    if (secs_since_last_sfx < MINIMUM_SECS_BETWEEN_SFX):
        await ctx.send(f'@{ctx.author.name} Please wait {round(MINIMUM_SECS_BETWEEN_SFX - secs_since_last_sfx, 1)} seconds before using another sfx ⏳')
        return

    last_sfx_time = time()
    
    Thread(target=playsound, args=(fullsfxpath,), daemon=True).start()
    spend_user_currency(ctx.author.name, gil_cost)
    print(f'{ctx.author.name} played sfx "{sfxname}" costing {get_currency_str(gil_cost)}')

# COMMAND - FLIP A COIN
@bot.command(name='coinflip')
async def coinflip(ctx):
    if randint(1,2) == 1:
        coin = 'HEADS'
    else:
        coin = 'TAILS'
    result_str = f'The coin landed on {coin}'
    await ctx.send(result_str)

# INIT ------------------------------
if __name__ == "__main__":
    Thread(target=playsound, args=(f'{os.getcwd()}\sfx\coin.mp3',), daemon=True).start()
    print(f"Starting {os.environ['BOT_NICK']}")
    populate_user_data_cache()
    save_users_backup()
    bot.run()