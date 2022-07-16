# Metatrader 5 API

API HTTP Wrapper to Metatrader5 python apis.


### Commands

```sh
# Install dependencies
poetry add <dependency name>
# Activate Env
poetry shell
# Start app
uvicorn main:app --reload
```

### Apis:

![OpenAPI](/images/openapi.png "OpenAPI")

```sh
# Get Prices
curl -X 'GET' \
  'http://localhost:8000/prices?symbol=PETR3&timeframe=TIMEFRAME_M1&initial_date=2022-06-16%2018%3A30%3A53.837069&final_date=2022-07-16%2018%3A30%3A53.837069' \
  -H 'accept: application/json'
```

## Docs

Symbols Properties: https://www.mql5.com/en/docs/constants/environment_state/marketinfoconstants#symbol_filling_mode

Order Send Properties: https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py#traderequest

Prices: https://www.mql5.com/en/docs/integration/python_metatrader5/mt5copyratesrange_py

