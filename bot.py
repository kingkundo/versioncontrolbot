# bot.py
# Tom Taylor / Version Control
# 2021

# Entry point for the versioncontrolbot project.

from os import environ, getcwd

# These 'unused imports' are here to initialise the various
# global variables and events for the bot to hook into.
import common
import chatuser
import commands
import gil
import events

# INIT ------------------------------
if __name__ == "__main__":
    'Initialisation of versioncontrolbot happens here '
    common.play_sound(f'{getcwd()}\sfx\coin.mp3')
    print(f"Starting {environ['BOT_NICK']}")
    chatuser.populate_user_data_cache()
    chatuser.save_backup()
    common.bot.run()