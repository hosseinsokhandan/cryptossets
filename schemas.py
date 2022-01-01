from pydantic import BaseModel


class Asset(BaseModel):
    name: str
    quantity: float
