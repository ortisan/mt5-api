import MetaTrader5 as mt5
from fastapi import APIRouter, HTTPException

from mt5_api.models import Order

router = APIRouter()


@router.get("/orders", tags=["orders"])
async def get_orders(symbol: str = None):
    orders = mt5.orders_get(symbol)
    if not orders:
        raise HTTPException(status_code=404, detail=f"Orders not found.")
    return orders


@router.post("/orders", tags=["orders"])
async def post_order(order: Order):
    request_order_mt5 = order.to_mt5_order()
    result = mt5.order_send(request_order_mt5)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise HTTPException(
            status_code=422, detail=f"Error to send order: {result.retcode}"
        )
    result_dict = result._asdict()
    return result_dict
