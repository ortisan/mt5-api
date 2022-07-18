from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd
from fastapi import APIRouter
from loguru import logger

from mt5_api.models import TimeframeEnum

router = APIRouter()


@router.get("/prices", tags=["prices"])
async def get_prices(
    symbol: str, timeframe: TimeframeEnum, initial_date: datetime, final_date: datetime
):
    rates = mt5.copy_rates_range(symbol, timeframe.to_mt5(), initial_date, final_date)
    rates_df = pd.DataFrame(rates)
    rates_df["date"] = pd.to_datetime(rates_df["time"], unit="s")
    rates_df = rates_df.set_index("time")
    return rates_df.to_dict(orient="index")
