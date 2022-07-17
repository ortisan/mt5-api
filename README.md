# Metatrader 5 API

API HTTP Wrapper to Metatrader5 python apis.

## Pre reqs

1. Install [Metatrader 5](https://www.metatrader5.com/en/download)
2. Get MT5 licence from your investment account. Eg. [Rico](https://www.rico.com.vc/) 

### Commands

```sh
# Install dependencies
poetry add <dependency name>
# Activate Env
poetry shell
# Organize imports
poetry run isort .
# Autoformat
poetry run black .
# Test
poetry run coverage run -m pytest && poetry run coverage report -m
# Start app
uvicorn main:app --reload
```

### Apis

![OpenAPI](/images/openapi.png "OpenAPI")

```sh
# Get Symbols
curl -X 'GET' \
  'http://localhost:8000/symbols?type=VISTA' \
  -H 'accept: application/json'
  
# Get Prices
curl -X 'GET' \
  'http://localhost:8000/prices?symbol=PETR3&timeframe=TIMEFRAME_M1&initial_date=2022-06-16%2018%3A30%3A53.837069&final_date=2022-07-16%2018%3A30%3A53.837069' \
  -H 'accept: application/json'

# Send Order
curl -X 'POST' \
  'http://localhost:8000/orders' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "type": "BUY",
  "symbol": "PETR4",
  "volume": 100,
  "comment": "Teste de api"
}'
```

## Docs

- [Symbols Properties](https://www.mql5.com/en/docs/constants/environment_state/marketinfoconstants)
- [Order Send Properties](https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py#traderequest)
- [Prices](https://www.mql5.com/en/docs/integration/python_metatrader5/mt5copyratesrange_py)
