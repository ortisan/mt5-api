import collections

import MetaTrader5 as mt5
from fastapi.testclient import TestClient

from mt5_api.main import app

client = TestClient(app)

_mt5_symbols_get = [
    type(
        "obj",
        (object,),
        {"name": "PETR3", "point": 0.1, "path": "BOVESPA\\A VISTA\\PETR3"},
    ),
    type(
        "obj",
        (object,),
        {"name": "ITUB3", "point": 0.2, "path": "BOVESPA\\A VISTA\\ITUB3"},
    ),
]


def test_get_all_symbols(mocker):
    mocker.patch.object(
        mt5,
        "symbols_get",
        return_value=_mt5_symbols_get,
    )
    response = client.get("/symbols")
    assert response.status_code == 200
    symbols = response.json()
    assert len(symbols) == 2
    assert symbols[0] == "PETR3"
    assert symbols[1] == "ITUB3"


def test_get_all_symbols_paths(mocker):
    mocker.patch.object(
        mt5,
        "symbols_get",
        return_value=_mt5_symbols_get,
    )
    response = client.get("/symbols_paths")
    assert response.status_code == 200
    paths = response.json()
    assert len(paths) == 1
    assert paths[0] == "BOVESPA\\A VISTA"


def test_get_symbol(mocker):
    mocker.patch.object(
        mt5,
        "symbol_info",
        return_value=_mt5_symbols_get[0],
    )

    mocker.patch.object(
        mt5, "symbol_info_tick", return_value=type("obj", (), {"ask": 100.0})
    )

    symbol = "PETR3"
    response = client.get(f"/symbols/{symbol}")
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["symbol"] == symbol
    assert json_response["point"] == 0.1
    assert json_response["price"] == 100.0


def test_get_symbol_no_bid(mocker):
    mocker.patch.object(
        mt5,
        "symbol_info",
        return_value=_mt5_symbols_get[0],
    )

    mocker.patch.object(mt5, "symbol_info_tick", return_value=None)

    symbol = "PETR3"
    response = client.get(f"/symbols/{symbol}")
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["symbol"] == symbol
    assert json_response["point"] == 0.1
    assert json_response["price"] == 0.0


def test_get_symbol_not_found(mocker):
    mocker.patch.object(
        mt5,
        "symbol_info",
        return_value=None,
    )
    symbol = "TEST123"
    response = client.get(f"/symbols/{symbol}")
    assert response.status_code == 404


_mt5_orders = [
    {"symbol": "PETR4"},
]


class OrderSendResult(object):
    def __init__(self, retcode: int, result: dict):
        self.retcode = retcode
        self.result = result

    def _asdict(self, *args, **kwargs):
        return self.result


trade_position_fields = [
    "ticket",
    "time",
    "time_msc",
    "time_update",
    "time_update_msc",
    "type",
    "magic",
    "identifier",
    "reason",
    "volume",
    "price_open",
    "sl",
    "tp",
    "price_current",
    "swap",
    "profit",
    "symbol",
    "comment",
    "external_id",
]

TradePosition = collections.namedtuple("TradePosition", trade_position_fields)


def test_post_order(mocker):
    mocker.patch.object(
        mt5, "symbol_info_tick", return_value=type("obj", (), {"ask": 100.0})
    )

    mocker.patch.object(
        mt5,
        "symbol_info",
        return_value=_mt5_symbols_get[0],
    )

    mocker.patch.object(
        mt5,
        "order_send",
        return_value=OrderSendResult(
            mt5.TRADE_RETCODE_DONE, {"symbol": _mt5_symbols_get[0].name}
        ),
    )

    buy_order = {
        "type": "BUY",
        "symbol": _mt5_symbols_get[0].name,
        "volume": 100,
        "comment": "Testing",
    }
    response = client.post("/orders", json=buy_order)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["symbol"] == _mt5_symbols_get[0].name


def test_post_order_error_send(mocker):
    mocker.patch.object(
        mt5, "symbol_info_tick", return_value=type("obj", (), {"ask": 100.0})
    )

    mocker.patch.object(
        mt5,
        "symbol_info",
        return_value=_mt5_symbols_get[0],
    )

    mocker.patch.object(
        mt5,
        "order_send",
        return_value=OrderSendResult(mt5.TRADE_RETCODE_REJECT, {}),
    )

    buy_order = {
        "type": "BUY",
        "symbol": _mt5_symbols_get[0].name,
        "volume": 100,
        "comment": "Testing",
    }
    response = client.post("/orders", json=buy_order)
    assert response.status_code == 400


def test_get_orders(mocker):
    mocker.patch.object(
        mt5,
        "orders_get",
        return_value=_mt5_orders,
    )
    symbol = "PETR4"
    response = client.get(f"/orders?symbol={symbol}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response[0]["symbol"] == "PETR4"


def test_get_orders_not_found(mocker):
    mocker.patch.object(
        mt5,
        "orders_get",
        return_value=None,
    )
    symbol = "PETR4"
    response = client.get(f"/orders?symbol={symbol}")
    assert response.status_code == 404


def test_get_positions(mocker):
    mocker.patch.object(
        mt5,
        "positions_get",
        return_value=(
            TradePosition(
                1247594537,
                1658141642,
                1658141642072,
                1658163105,
                1658163105889,
                0,
                0,
                1247594537,
                3,
                400.0,
                28.5375,
                27.54,
                29.54,
                28.55,
                0.0,
                5.0,
                "PETR4",
                "Compra PETR4",
                "",
            ),
        ),
    )
    response = client.get(f"/positions")
    assert response.status_code == 200


def test_get_positions_not_found(mocker):
    mocker.patch.object(
        mt5,
        "positions_get",
        return_value=None,
    )

    response = client.get(f"/positions")
    assert response.status_code == 404
