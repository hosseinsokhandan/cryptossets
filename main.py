from fastapi import FastAPI

from exchanges import kucoin

app = FastAPI()


@app.get('/kucoin')
def kucoin_assets():
    orders = kucoin.get_orders("")
    print(len(orders))
    return orders
