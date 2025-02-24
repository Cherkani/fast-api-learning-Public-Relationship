from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel



class OrderBase(BaseModel):
    customer_id: int
    total_price: Optional[float] = None
    status: Optional[str] = None
    tracking_number: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    total_price: Optional[float] = None
    status: Optional[str] = None
    tracking_number: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None


    class Config:
        from_attributes = True
