from fastapi.testclient import TestClient

from mt5_api.main import app

client = TestClient(app)


def test_get_all_symbols():
    response = client.get("/symbols")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_all_symbols_paths():
    response = client.get("/symbols_paths")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_symbol():
    symbol = "PETR4"
    response = client.get(f"/symbols/{symbol}")
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["symbol"] == symbol
    assert json_response["point"] > 0.0
    assert json_response["price"] > 0.0


def test_get_orders():
    symbol = "PETR4"
    response = client.get(f"/orders?symbol={symbol}")
    assert response.status_code == 200
