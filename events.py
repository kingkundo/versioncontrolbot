# events.py
# Tom Taylor / Version Control
# 2021

from os import environ
from time import time
from common import bot, set_streamer_info
from chatuser import give_all_chat_users_gil

# EVENTS ------------------------------

# EVENT - ON BOT ENTERING CHAT
@bot.event
async def event_ready():
    'Event thats called once when the bot goes online.'
    streamer_info = await bot.get_users(environ['CHANNEL'])
    set_streamer_info(streamer_info[0])

    print(f"{environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(environ['CHANNEL'], f"/me has arrived! 🎉")

# EVENT - ON MESSAGE IN CHAT
last_payout_time = time()
@bot.event
async def event_message(ctx):
    'Event thats called every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == environ['BOT_NICK'].lower():
        return

    await bot.handle_commands(ctx)

    # Handle custom commands...

    if 'hello bot' in ctx.content.lower():
        await ctx.channel.send(f"Hey, @{ctx.author.name} ❤️")

    # If the stream is live, and people have been in chat for X mins, then they get a payout
    global last_payout_time
    minimum_secs_between_payouts = int(environ['MINIMUM_SECS_BETWEEN_PAYOUTS'])
    secs_since_last_payout = (time() - last_payout_time)
    if (secs_since_last_payout > minimum_secs_between_payouts) and (await bot.get_stream(environ['CHANNEL']) is not None):
        await give_all_chat_users_gil(int(environ['AMOUNT_TO_PAY_OUT_REGULARLY']))
        last_payout_time = time()