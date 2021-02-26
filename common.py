# common.py
# Tom Taylor / Version Control
# 2021

from os import environ
from threading import Thread
from playsound import playsound
from twitchio.ext import commands

# CONFIG ------------------------------
bot = commands.Bot(
        irc_token=environ['TMI_TOKEN'],
        client_id=environ['CLIENT_ID'],
        nick=environ['BOT_NICK'],
        prefix=environ['BOT_PREFIX'],
        initial_channels=[environ['CHANNEL']],
        client_secret=environ['CLIENT_SECRET']
    )

# GLOBALS ----------------------------
streamer_info = None

# HELPERS ----------------------------
def set_streamer_info(new_streamer_info):
    'Should be called as soon as a connection to chat is made. This will get data about the streamer'
    global streamer_info
    streamer_info = new_streamer_info

def play_sound(sfxpath):
    'Play a sound effect'
    Thread(target=playsound, args=(sfxpath,), daemon=True).start()

async def does_user_follow_streamer(follower_user_id : int) -> bool:
    'Returns true is the user passed by parameter is following the streamer, false if not'
    if follower_user_id == int(streamer_info.id):
        return True

    user_follows_streamer = await bot.get_follow(follower_user_id, streamer_info.id)
    return (user_follows_streamer is not None) and ('followed_at' in user_follows_streamer) and (user_follows_streamer['followed_at'] != '')