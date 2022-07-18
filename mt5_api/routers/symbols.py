import MetaTrader5 as mt5
from fastapi import APIRouter, HTTPException

from mt5_api.models import SymbolType

router = APIRouter()
from loguru import logger


@router.get("/symbols", tags=["symbols"])
async def get_all_symbols(symbol_type: SymbolType = SymbolType.VISTA):
    symbol_type_filter = symbol_type.get_filter()
    all_symbols = mt5.symbols_get()
    return [s.name for s in all_symbols if symbol_type_filter in s.path]


@router.get("/symbols_paths", tags=["symbols"])
async def get_all_symbols_paths():
    all_symbols = mt5.symbols_get()
    paths = {"\\".join(s.path.split("\\")[:-1]) for s in all_symbols}
    return paths


@router.get("/symbols/{symbol}", tags=["symbols"])
async def get_symbol(symbol: str):
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        raise HTTPException(status_code=404, detail=f"Orders not found.")

    symbol_tick_info = mt5.symbol_info_tick(symbol)
    if not symbol_tick_info:
        logger.error(f"Error to get bid/ask price of {symbol}: {mt5.last_error()}")
    return {
        "symbol": symbol_info.name,
        "point": symbol_info.point,
        "price": symbol_tick_info.ask if symbol_tick_info else 0.0,
    }
