from pydantic import BaseModel, Field
from enum import Enum


class ValutaEnum(str, Enum):
    rub = "рубли"
    usd = "доллары"


class OfferBase(BaseModel):
    summa: float = Field(..., gt=0, description="Сумма оффера, должна быть больше 0")
    valuta: ValutaEnum
    comment: str | None = Field(None, max_length=500)


class OfferCreate(OfferBase):
    pass


class Offer(OfferBase):
    id: int

    class Config:
        from_attributes = True
