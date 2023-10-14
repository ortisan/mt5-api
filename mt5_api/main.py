import MetaTrader5 as mt5
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError

from mt5_api.routes import orders, positions, prices, symbols
from mt5_api.settings import Settings

app = FastAPI()
app.include_router(symbols.router)
app.include_router(orders.router)
app.include_router(positions.router)
app.include_router(prices.router)

settings = Settings()

# Establish connection to the MetaTrader 5 terminal
logger.info("Starting MT5 terminal...")
initialized = mt5.initialize()
# initialized = mt5.initialize(
#     settings.mt5_path,
#     login=settings.mt5_login,
#     password=settings.mt5_password,
#     server=settings.mt5_server,
#     timeout=settings.mt5_timeout,
#     portable=False
# )
if not initialized:
    error_msg = f"MT5 initialization failed: {mt5.last_error()}"
    logger.error(error_msg)
    raise Exception(error_msg)
logger.info("Terminal initialized...")


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.error(exc)
    return JSONResponse(
        status_code=422,
        content=exc.json(),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(Exception)
async def default_exception_handler(request: Request, exc: Exception):
    logger.exception(exc)
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )
