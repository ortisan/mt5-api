from pydantic import BaseModel
from typing import Union
import MetaTrader5 as mt5
from enum import Enum


class OrderType(str, Enum):
    Buy = "BUY"
    Sell = "SELL"


class Order(BaseModel):
    type: OrderType
    symbol: str
    volume: float
    price: float
    stoplimit: float
    price: float
    comment: Union[str, None] = None

    def to_mt5_order(self):
        mt5_order_request = {"symbol": self.symbol, "action": mt5.TRADE_ACTION_DEAL, "volume": self.volume}
        mt5_order_request["action"] = mt5.TRADE_ACTION_DEAL
        type = None
        if self.type == OrderType.Buy:
            type = mt5.ORDER_TYPE_BUY
        elif self.type == OrderType.Sell:
            type = mt5.ORDER_TYPE_SELL
        mt5_order_request["type"] = type

        return mt5_order_request
        
        




