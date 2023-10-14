from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd
from fastapi import APIRouter

from mt5_api.models import TimeframeEnum

router = APIRouter()


@router.get("/prices", tags=["prices"])
async def get_prices(
    symbol: str, timeframe: TimeframeEnum, initial_date: datetime, final_date: datetime
):
    rates = mt5.copy_rates_range(symbol, timeframe.to_mt5(), initial_date, final_date)
    rates_df = pd.DataFrame(rates)
    rates_df.rename(columns={"time": "timestamp"}, inplace=True)
    rates_df["datetime"] = pd.to_datetime(rates_df["timestamp"], unit="s")
    return rates_df.to_dict(orient="records")
