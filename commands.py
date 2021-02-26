# commands.py
# Tom Taylor / Version Control
# 2021

from os import environ, path as ospath, getcwd
from time import time
from random import randint
from glob import glob
from common import bot, does_user_follow_streamer, play_sound
from gil import get_currency_str
from chatuser import spend_user_currency, get_user_currency, add_user_currency, give_all_chat_users_gil

# COMMANDS ------------------------------

@bot.command(name='help')
async def help(ctx):
    'The help command. Most straightforward command for a chatbot'
    await ctx.send(f"@{ctx.author.name} {environ['HELP_STR']}")

@bot.command(name='balance')
async def balance(ctx):
    'The balance command. Returns the currency balance of the user who said the command'
    await ctx.send(f'@{ctx.author.name} You have {get_user_currency(ctx.author.name)} in the bank 💰')

@bot.command(name='addgil')
async def addgil(ctx):
    'Allows a mod to add currency to a user. The command should look like this "!addgil username 100"'
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

@bot.command(name='spendgil')
async def spendgil(ctx):
    'Allows a mod to remove currency from a user. The command should look like "!spendgil username 100"'
    if not ctx.author.is_mod:
        await ctx.send(f'@{ctx.author.name} You must be a mod to perform this action 🛑')
        return

    components = ctx.content.split()

    if (len(components) == 3) and (components[2].isnumeric()):
        result = spend_user_currency(components[1], int(components[2]))
        result_str = f"{components[1]} has spent {int(components[2])} from their original balance of {result['old']} and now has {result['new']}"
        print(result_str)
        await ctx.send(result_str)

@bot.command(name='gamble')
async def gamble(ctx):
    'Allows chat users to gamble their currency. The command should look like "!gamble 150"'
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

@bot.command(name='sfxlist')
async def sfxlist(ctx):
    'Command to post a link to the SFX list'
    await ctx.send(environ['SFX_HELP_STR'])

last_sfx_time = time()
@bot.command(name='sfx')
async def playsfx(ctx):
    'Command to play a sound effect to the standard audio output device'
    if not await does_user_follow_streamer(ctx.author.id):
        await ctx.send(f'@{ctx.author.name} You must be a follower of the stream to perform this action 🛑')
        return

    music_file_extension = '.mp3'
    sfxname = ctx.content.partition('sfx ')[2]
    sfxpath = f'{getcwd()}\sfx\{sfxname}*[0-9]*{music_file_extension}'
    fullsfxpath = ''
    gil_cost = 0
    for file in glob(sfxpath):
        fullsfxpath = file
        gil_cost = int(fullsfxpath[fullsfxpath.find(sfxname)+len(sfxname):fullsfxpath.rfind(music_file_extension)])

    if (sfxname == '') or (fullsfxpath == '') or (not ospath.exists(fullsfxpath)):
        await ctx.send(f'@{ctx.author.name} That sfx is invalid 😢')
        return

    user_balance = get_user_currency(ctx.author.name, False)
    if gil_cost > user_balance:
        await ctx.send(f"@{ctx.author.name} You don't have the gil balance to use this sfx. Your balance is {user_balance} and this sfx costs {gil_cost}")
        return

    global last_sfx_time

    minimum_secs_between_sfx = int(environ['MINIMUM_SECS_BETWEEN_SFX'])
    secs_since_last_sfx = (time() - last_sfx_time)
    if (secs_since_last_sfx < minimum_secs_between_sfx):
        await ctx.send(f'@{ctx.author.name} Please wait {round(minimum_secs_between_sfx - secs_since_last_sfx, 1)} seconds before using another sfx ⏳')
        return

    last_sfx_time = time()
    
    play_sound(fullsfxpath)
    spend_user_currency(ctx.author.name, gil_cost)
    print(f'{ctx.author.name} played sfx "{sfxname}" costing {get_currency_str(gil_cost)}')

@bot.command(name='coinflip')
async def coinflip(ctx):
    'Command to flip a virtual coin. Equal change heads as tails.'
    if randint(1,2) == 1:
        coin = 'HEADS'
    else:
        coin = 'TAILS'
    result_str = f'The coin landed on {coin}'
    await ctx.send(result_str)