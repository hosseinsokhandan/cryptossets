from datetime import date, datetime, timedelta
from kucoin.client import Client
import time

api_key = '619fbe7c2fe2ba0001e0a57e'
api_secret = '52558931-13b7-4fcd-82ad-45422ff99e12'
api_passphrase = 'hs46773464677346'

client = Client(api_key, api_secret, api_passphrase)


def get_orders(symbol=None):
    start_time: int = 1617222661000
    now = int(round(time.time() * 1000))
    seven_day_in_milisec = 604800000
    orders = []
    while start_time < now:
        _o = client.get_orders(
            symbol=symbol, start=start_time,
            end=start_time + seven_day_in_milisec
        )["items"]

        if _o:
            for o in _o:
                orders.append(o)

        start_time += seven_day_in_milisec
        time.sleep(0.2)

    return orders


def get_balance():
    balance = client.get_accounts()
    balance = filter(lambda b: b["type"] == "trade", balance)
    return list(balance)
