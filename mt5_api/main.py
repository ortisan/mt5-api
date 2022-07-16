from fastapi import FastAPI
from models import Order

app = FastAPI()

@app.get("/symbols")
async def get_all_symbols():
  symbols= ["PETR4"]
  return symbols

@app.get("/symbols/{symbol}")
async def get_all_symbols(symbol: str):
  return {}

@app.get("/orders")
async def get_orders():
  return []

@app.post("/orders")
async def post_order(order: Order):
  return [order]

@app.get("/positions")
async def get_positions():
  return []

@app.get("/prices")
async def get_prices():
  return []

