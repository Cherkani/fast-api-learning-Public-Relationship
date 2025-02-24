from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    total_price = Column(DECIMAL(10, 2), nullable=True)
    status = Column(String(50), nullable=True)
    tracking_number = Column(String(100), nullable=True)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="orders")

    menu_items = relationship("OrderMenuItem", back_populates="order")

class OrderMenuItem(Base):
    __tablename__ = "order_menu_item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.menuItemID"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    quantity = Column(Float, nullable=False) 

    menu_item = relationship("MenuItem", back_populates="order_items")  
    order = relationship("Order", back_populates="menu_items")