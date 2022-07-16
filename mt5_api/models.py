from pydantic import BaseModel
from typing import Union

class Order(BaseModel):
    symbol: str
    volume: float
    price: float
    stoplimit: float
    price: float
    comment: Union[str, None] = None


