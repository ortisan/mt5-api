from enum import Enum
from typing import List, Union

import MetaTrader5 as mt5
from pydantic import BaseModel


class TimeframeEnum(str, Enum):
    TIMEFRAME_M1 = "TIMEFRAME_M1"
    TIMEFRAME_M2 = "TIMEFRAME_M2"
    TIMEFRAME_M3 = "TIMEFRAME_M3"
    TIMEFRAME_M4 = "TIMEFRAME_M4"
    TIMEFRAME_M5 = "TIMEFRAME_M5"
    TIMEFRAME_M6 = "TIMEFRAME_M6"
    TIMEFRAME_M10 = "TIMEFRAME_M10"
    TIMEFRAME_M12 = "TIMEFRAME_M12"
    TIMEFRAME_M15 = "TIMEFRAME_M15"
    TIMEFRAME_M20 = "TIMEFRAME_M20"
    TIMEFRAME_M30 = "TIMEFRAME_M30"
    TIMEFRAME_H1 = "TIMEFRAME_H1"
    TIMEFRAME_H2 = "TIMEFRAME_H2"
    TIMEFRAME_H4 = "TIMEFRAME_H4"
    TIMEFRAME_H3 = "TIMEFRAME_H3"
    TIMEFRAME_H6 = "TIMEFRAME_H6"
    TIMEFRAME_H8 = "TIMEFRAME_H8"
    TIMEFRAME_H12 = "TIMEFRAME_H12"
    TIMEFRAME_D1 = "TIMEFRAME_D1"
    TIMEFRAME_W1 = "TIMEFRAME_W1"
    TIMEFRAME_MN1 = "TIMEFRAME_MN1"

    def to_mt5(self):
        return getattr(mt5, self)


class SymbolType(str, Enum):
    VISTA = "VISTA"
    FRACTION = "FRACTION"
    OPTION = "OPTION"
    INDEX = "INDEX"


class SymbolTypeModel(BaseModel):
    types: List[SymbolType]


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
        order_type = None
        if self.type == OrderType.Buy:
            order_type = mt5.ORDER_TYPE_BUY
        elif self.type == OrderType.Sell:
            order_type = mt5.ORDER_TYPE_SELL
        mt5_order_request["type"] = order_type
        return mt5_order_request


class SymbolTypeModel(BaseModel):
    types: List[SymbolType]


symbols_type_filter = {
    SymbolType.VISTA: "BOVESPA\\A VISTA",
    SymbolType.FRACTION: "BOVESPA\\FRACIONARIO",
    SymbolType.OPTION: "BOVESPA\\OPCOES",
    SymbolType.INDEX: "BOVESPA\\INDICES",
}
