from fastapi import FastAPI
from models import Order
import MetaTrader5 as mt5
from settings import Settings
from enum import Enum
from typing import List
from pydantic import BaseModel
from loguru import logger

logger.add("mt5-api.log", rotation="100 MB", enqueue=True,  serialize=True)

app = FastAPI()
settings = Settings()

class SymbolType(str, Enum):
    VISTA = "VISTA"
    FRACTION = "FRACTION"
    OPTION = "OPTION"
    INDEX = "INDEX"

symbols_type_filter = {
    SymbolType.VISTA: "BOVESPA\\A VISTA",
    SymbolType.FRACTION: "BOVESPA\\FRACIONARIO",
    SymbolType.OPTION: "BOVESPA\\OPCOES",
    SymbolType.INDEX: "BOVESPA\\INDICES",
}

class SymbolTypeModel(BaseModel):
    types: List[SymbolType]

# initialized = mt5.initialize(
#     settings.mt5_path,
#     login=settings.mt5_login,
#     password=settings.mt5_password,
#     server=settings.mt5_server,
#     timeout=settings.mt5_timeout,
#     portable=False
# )

initialized = mt5.initialize()

# establish connection to the MetaTrader 5 terminal
if not initialized:
    logger.error(f"MT5 initialization failed: {mt5.last_error()}")


@app.get("/symbols")
async def get_all_symbols(type: SymbolType = SymbolType.VISTA):
    symbol_type_filter = symbols_type_filter[type]
    all_symbols = mt5.symbols_get()
    return [s.name for s in all_symbols if symbol_type_filter in s.path]


@app.get("/symbols_paths")
async def get_all_symbols_paths():
    all_symbols = mt5.symbols_get()
    paths = {"\\".join(s.path.split("\\")[:-1]) for s in all_symbols}
    return paths


@app.get("/symbols/{symbol}")
async def get_symbol(symbol: str):
    symbol_info=mt5.symbol_info(symbol)
    return {
        "name": symbol_info.name,
        "point": symbol_info.point,
        "price": symbol_info.ask
    }


@app.get("/orders")
async def get_orders():
    return mt5.orders_get()


@app.post("/orders")
async def post_order(order: Order):
    mt5.order_send()
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 100 * point,
        "tp": price + 100 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }


    return [order]


@app.get("/positions")
async def get_positions():
    return []


@app.get("/prices")
async def get_prices():
    return []
