from typing import Dict, List
from kucoin.client import Client
import pandas as pd
import time
import warnings

STABLE_COINS = ["USDT", "USDC", "BUSD", "DAI", "UST", "TUSD"]

api_key = '619fbe7c2fe2ba0001e0a57e'
api_secret = '52558931-13b7-4fcd-82ad-45422ff99e12'
api_passphrase = 'hs46773464677346'

client = Client(api_key, api_secret, api_passphrase)


def get_orders(symbol=None) -> List[Dict]:
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


def get_balance() -> List[Dict]:
    balance = client.get_accounts()
    balance = filter(lambda b: b["type"] == "trade", balance)
    return list(balance)


def calculate(balance: list, orders: list) -> List[Dict]:
    data = []
    for b in balance:
        _data = {}
        _data["currency"] = b["currency"]
        _data["balance"] = b["balance"]

        if b["currency"] in STABLE_COINS:
            data.append(_data)
            continue

        asset_history = list(
            filter(
                lambda a: a["symbol"].split("-")[0] == b["currency"], orders
            )
        )
        df = pd.DataFrame(asset_history, columns=["price", "size", "side"])
        df = df.loc[df["side"] == "buy"]
        df["size"] = df["size"].astype('float')
        df["price"] = df["price"].astype('float')
        df["mul"] = df["price"] * df["size"]
        mul = df["mul"].sum()
        size = df["size"].sum()
        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                _data["avg_buy"] = round(mul / size, 2)
            except:
                _data["avg_buy"] = float(0)
        _data["size"] = size
        _data["current_price"] = client.get_ticker(
            f'{b["currency"]}-USDT'
        )["price"]
        _data["profit"] = round(
            (float(_data["current_price"]) * _data["size"]) -
            (_data["avg_buy"] * _data["size"]),
            2
        )
        _data["profit_class"] = "success" if _data["profit"] >= 0 else "danger"
        _data["profit_proportion"] = round(
            (_data["profit"] * 100) / (_data["avg_buy"] * _data["size"]),
            2
        )
        data.append(_data)

    return sorted(data, key=lambda i: i.get('profit', 0), reverse=True)
