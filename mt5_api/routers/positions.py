import MetaTrader5 as mt5
import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter()
from loguru import logger


@router.get("/positions", tags=["positions"])
async def get_positions(symbol: str = None):
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        raise HTTPException(status_code=404, detail=f"Positions not found.")
    positions_df = pd.DataFrame(list(positions), columns=positions[0]._asdict().keys())
    positions_df["time"] = pd.to_datetime(positions_df["time"], unit="s")
    positions_df.drop(
        ["time_update", "time_msc", "time_update_msc", "external_id"],
        axis=1,
        inplace=True,
    )
    return positions_df.to_dict(orient="index")
