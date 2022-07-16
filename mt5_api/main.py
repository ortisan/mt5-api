from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
from fastapi import FastAPI
from loguru import logger

from models import Order, SymbolType, TimeframeEnum, symbols_type_filter
from settings import Settings

logger.add("mt5-api.log", rotation="100 MB", enqueue=True, serialize=True)

app = FastAPI()
settings = Settings()

# establish connection to the MetaTrader 5 terminal
logger.info("Starting MT5 terminal...")
initialized = mt5.initialize()
# initialized = mt5.initialize(
#     settings.mt5_path,
#     login=settings.mt5_login,
#     password=settings.mt5_password,
#     server=settings.mt5_server,
#     timeout=settings.mt5_timeout,
#     portable=False
# )
if not initialized:
    error_msg = f"MT5 initialization failed: {mt5.last_error()}"
    logger.error(error_msg)
    raise Exception(error_msg)

logger.info("Terminal initialized...")


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
    symbol_info = mt5.symbol_info(symbol)
    return {
        "name": symbol_info.name,
        "point": symbol_info.point,
        "price": symbol_info.ask
    }


@app.get("/orders")
async def get_orders(symbol: str = None):
    return mt5.orders_get(symbol=symbol)


@app.post("/orders")
async def post_order(order: Order):
    request_order_mt5 = order.to_mt5_order()
    return mt5.order_send(request_order_mt5)


@app.get("/positions")
async def get_positions(symbol: str = None):
    return mt5.positions_get(symbol)

@app.get("/prices")
async def get_prices(symbol: str, timeframe: TimeframeEnum, initial_date: datetime, final_date: datetime):
    try:
        rates = mt5.copy_rates_range(symbol, timeframe.to_mt5(), initial_date, final_date)
        rates_df = pd.DataFrame(rates)
        rates_df["date"] = pd.to_datetime(rates_df["time"], unit="s")
        rates_df = rates_df.set_index("time")
        return rates_df.to_dict(orient='index')
    except Exception as exc:
        logger.exception(exc)
