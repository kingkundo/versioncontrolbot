# chatuser.py
# The user object representing a person in chat monitored by Version Control Bot

import json
from datetime import datetime
from collections import defaultdict
from gil import MINIMUM_POSSIBLE_BALANCE, JSON_KEY as CURRENCY_JSON_KEY, get_currency_str

USERDATA_JSON_NAME = 'chatusers'
USERDATA_JSON_FILE = f'{USERDATA_JSON_NAME}.json'
USER_JSON_KEY = 'user'

# This object holds the cache of all user data.
# This is to prevent reading and writing from files all the time.
userdata = {}

def __set_up_user(user_name : str):
    if not user_name in userdata:
        userdata[user_name] = {}

    if not CURRENCY_JSON_KEY in userdata[user_name]:
        userdata[user_name][CURRENCY_JSON_KEY] = MINIMUM_POSSIBLE_BALANCE

def save_backup():
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
    'Returns the users current currency balance, formatted'
    __set_up_user(user_name)
    if not formatted:
        return userdata[user_name][CURRENCY_JSON_KEY]
    else:
        try:
            return get_currency_str(userdata[user_name][CURRENCY_JSON_KEY])
        except KeyError:
            return get_currency_str(MINIMUM_POSSIBLE_BALANCE)