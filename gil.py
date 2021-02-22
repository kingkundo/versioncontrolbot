# gil.py
# The currency used by Version Control Bot

from enum import Enum

class CurrencyFormat(Enum):
    SYMBOL_FIRST_NO_SPACE = 1
    SYMBOL_FIRST_W_SPACE = 2
    SYMBOL_LAST_NO_SPACE = 3
    SYMBOL_LAST_W_SPACE = 4

JSON_KEY = 'CURRENCY'
CURRENCY_SIGN = 'gil'
CURRENCY_FORMAT = CurrencyFormat.SYMBOL_LAST_W_SPACE

MINIMUM_POSSIBLE_BALANCE = 50

# Helpers ------------------

def get_currency_str(value : str) -> str:
    if value == '':
        value = str(MINIMUM_POSSIBLE_BALANCE)

    'Returns the currency value, formatted correctly.'
    if CURRENCY_FORMAT == CurrencyFormat.SYMBOL_FIRST_NO_SPACE:
        return f'{CURRENCY_SIGN}{value:.0f}'
    elif CURRENCY_FORMAT == CurrencyFormat.SYMBOL_FIRST_W_SPACE:
        return f'{CURRENCY_SIGN} {value:.0f}'
    elif CURRENCY_FORMAT == CurrencyFormat.SYMBOL_LAST_NO_SPACE:
        return f'{value:.0f}{CURRENCY_SIGN}'
    elif CURRENCY_FORMAT == CurrencyFormat.SYMBOL_LAST_W_SPACE:
        return f'{value:.0f} {CURRENCY_SIGN}'
    else:
        return str(value)