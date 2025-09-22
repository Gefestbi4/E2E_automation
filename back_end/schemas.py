
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional


class ValutaEnum(str, Enum):
    rub = "рубли"
    eur = "евро"
    usd = "доллары"


class OfferBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    summa: float = Field(..., gt=0, description="Сумма оффера, должна быть больше 0")
    valuta: ValutaEnum
    comment: str | None = Field(None, max_length=500)


class OfferCreate(OfferBase):
    pass


class Offer(OfferBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
