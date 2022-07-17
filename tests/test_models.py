from unittest.mock import MagicMock

import MetaTrader5 as mt5

from mt5_api.models import (
    Order,
    OrderType,
    SymbolType,
    TimeframeEnum,
    _symbols_type_filter,
)


def test_timeframe():
    assert TimeframeEnum.TIMEFRAME_M1.to_mt5() == mt5.TIMEFRAME_M1
    assert TimeframeEnum.TIMEFRAME_M2.to_mt5() == mt5.TIMEFRAME_M2
    assert TimeframeEnum.TIMEFRAME_M3.to_mt5() == mt5.TIMEFRAME_M3
    assert TimeframeEnum.TIMEFRAME_M4.to_mt5() == mt5.TIMEFRAME_M4
    assert TimeframeEnum.TIMEFRAME_M5.to_mt5() == mt5.TIMEFRAME_M5
    assert TimeframeEnum.TIMEFRAME_M6.to_mt5() == mt5.TIMEFRAME_M6
    assert TimeframeEnum.TIMEFRAME_M10.to_mt5() == mt5.TIMEFRAME_M10
    assert TimeframeEnum.TIMEFRAME_M12.to_mt5() == mt5.TIMEFRAME_M12
    assert TimeframeEnum.TIMEFRAME_M15.to_mt5() == mt5.TIMEFRAME_M15
    assert TimeframeEnum.TIMEFRAME_M20.to_mt5() == mt5.TIMEFRAME_M20
    assert TimeframeEnum.TIMEFRAME_M30.to_mt5() == mt5.TIMEFRAME_M30
    assert TimeframeEnum.TIMEFRAME_H1.to_mt5() == mt5.TIMEFRAME_H1
    assert TimeframeEnum.TIMEFRAME_H2.to_mt5() == mt5.TIMEFRAME_H2
    assert TimeframeEnum.TIMEFRAME_H3.to_mt5() == mt5.TIMEFRAME_H3
    assert TimeframeEnum.TIMEFRAME_H4.to_mt5() == mt5.TIMEFRAME_H4
    assert TimeframeEnum.TIMEFRAME_H6.to_mt5() == mt5.TIMEFRAME_H6
    assert TimeframeEnum.TIMEFRAME_H8.to_mt5() == mt5.TIMEFRAME_H8
    assert TimeframeEnum.TIMEFRAME_H12.to_mt5() == mt5.TIMEFRAME_H12
    assert TimeframeEnum.TIMEFRAME_D1.to_mt5() == mt5.TIMEFRAME_D1
    assert TimeframeEnum.TIMEFRAME_W1.to_mt5() == mt5.TIMEFRAME_W1
    assert TimeframeEnum.TIMEFRAME_MN1.to_mt5() == mt5.TIMEFRAME_MN1


def test_symbol_type():
    assert SymbolType.VISTA.get_filter() == _symbols_type_filter[SymbolType.VISTA]
    assert SymbolType.OPTION.get_filter() == _symbols_type_filter[SymbolType.OPTION]
    assert SymbolType.INDEX.get_filter() == _symbols_type_filter[SymbolType.INDEX]


def test_order():
    mt5.symbol_info_tick = MagicMock(return_value=type("obj", (), {"ask": 100.0}))
    mt5.symbol_info = MagicMock(return_value=type("obj", (), {"point": 0.1}))

    buy_order = Order(type=OrderType.Buy, symbol="PETR4", volume=100, comment="Testing")
    request_mt5 = buy_order.to_mt5_order()

    assert request_mt5["type"] == mt5.ORDER_TYPE_BUY
    assert request_mt5["symbol"] == buy_order.symbol
    assert request_mt5["action"] == mt5.TRADE_ACTION_DEAL
    assert request_mt5["volume"] == 100
    assert request_mt5["price"] == 100.0
    assert request_mt5["sl"] == 90.0
    assert request_mt5["tp"] == 110.0
    assert request_mt5["deviation"] == 20

    sell_order = Order(
        type=OrderType.Sell, symbol="PETR4", volume=100, comment="Testing"
    )
    request_mt5 = sell_order.to_mt5_order()

    assert request_mt5["type"] == mt5.ORDER_TYPE_SELL
    assert request_mt5["symbol"] == sell_order.symbol
    assert request_mt5["action"] == mt5.TRADE_ACTION_DEAL
    assert request_mt5["volume"] == 100
    assert request_mt5["price"] == 100.0
    assert request_mt5["sl"] == 90.0
    assert request_mt5["tp"] == 110.0
    assert request_mt5["deviation"] == 20
