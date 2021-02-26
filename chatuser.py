# chatuser.py
# Tom Taylor / Version Control
# The user object representing a person in chat monitored by Version Control Bot

import json
from os import environ
from datetime import datetime
from common import bot
from currency import MINIMUM_POSSIBLE_BALANCE, JSON_KEY as CURRENCY_JSON_KEY, get_currency_str

USERDATA_JSON_NAME = 'chatusers'
USERDATA_JSON_FILE = f'{USERDATA_JSON_NAME}.json'
USER_JSON_KEY = 'user'

# This object holds the cache of all user data.
# This is to prevent reading and writing from files all the time.
userdata = {}

# HELPERS --------------------
def __set_up_user(user_name : str):
    'Local function that sets up a user locally in the json file and in memory'
    if not user_name in userdata:
        userdata[user_name] = {}

    if not CURRENCY_JSON_KEY in userdata[user_name]:
        userdata[user_name][CURRENCY_JSON_KEY] = MINIMUM_POSSIBLE_BALANCE

async def give_all_chat_users_currency(amount : int):
    'Loops through every user in chat, gives them the amount passed as parameter'
    chat_users = await bot.get_chatters(environ['CHANNEL'])
    for user in chat_users.all:
        add_user_currency(user, amount)
        print(f'{user} has been paid {amount} for tuning in')

def save_backup():
    'Save a backup of the current user information in a date/time-stamped json file'
    with open(f'{USERDATA_JSON_NAME}{datetime.today().strftime("%Y-%m-%d")}.json', 'w+') as user_backup_json_file:
        json.dump(userdata, user_backup_json_file)

def populate_user_data_cache():
    'Fills the "userdata" global cache object with all the data about chatusers'
    global userdata
    try:
        with open(USERDATA_JSON_FILE) as user_json_file:
            userdata = json.load(user_json_file)
    except FileNotFoundError:
        userdata = {}

def update_json_from_cache():
    'Take the in-memory array of chatusers and store it permenantly on disk to JSON'
    with open(USERDATA_JSON_FILE, 'w+') as user_json_file:
        json.dump(userdata, user_json_file)

def add_user_currency(user_name : str, amount : int):
    'Adds value to the users currency'
    __set_up_user(user_name)
    old_value = int(userdata[user_name][CURRENCY_JSON_KEY])
    new_value = int(old_value + amount)
    userdata[user_name][CURRENCY_JSON_KEY] = new_value

    update_json_from_cache()
    return {'old': old_value, 'new': get_currency_str(new_value)}

def spend_user_currency(user_name : str, amount : int):
    'Minuses value from the users currency'
    __set_up_user(user_name)
    old_value = int(userdata[user_name][CURRENCY_JSON_KEY])
    new_value = int(old_value - amount)

    if new_value < MINIMUM_POSSIBLE_BALANCE:
        new_value = MINIMUM_POSSIBLE_BALANCE
        
    userdata[user_name][CURRENCY_JSON_KEY] = new_value
    update_json_from_cache()
    return {'old': old_value, 'new': get_currency_str(new_value)}
    
def get_user_currency(user_name : str, formatted : bool = True) -> str:
    'Returns the users current currency balance, formatted if the second parameter is True'
    __set_up_user(user_name)
    if not formatted:
        return userdata[user_name][CURRENCY_JSON_KEY]
    else:
        try:
            return get_currency_str(userdata[user_name][CURRENCY_JSON_KEY])
        except KeyError:
            return get_currency_str(MINIMUM_POSSIBLE_BALANCE)