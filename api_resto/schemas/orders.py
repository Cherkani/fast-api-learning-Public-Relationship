from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel



class OrderBase(BaseModel):
    customer_id: int
    total_price: Optional[float] = None
    status: Optional[str] = None
    tracking_number: Optional[str] = None


class OrderMenuItem(BaseModel):
    menu_item_id: int
    quantity: float
    

class OrderCreate(OrderBase):
    menu_items : List[OrderMenuItem]



class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    total_price: Optional[float] = None
    status: Optional[str] = None
    tracking_number: Optional[str] = None
    menu_items : Optional[List[OrderMenuItem]] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    menu_items : Optional[List[OrderMenuItem]] = []


    class Config:
        from_attributes = True
