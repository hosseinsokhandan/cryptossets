from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from requests.sessions import Request
from starlette.responses import HTMLResponse

from exchanges import kucoin

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get('/kucoin', response_class=HTMLResponse)
async def kucoin_assets(request: Request):
    balance = kucoin.get_balance("")
    orders = kucoin.get_orders("")
    data = kucoin.calculate(balance, orders)
    context = {"request": request, "data": data}
    return templates.TemplateResponse("kucoin.html", context)
