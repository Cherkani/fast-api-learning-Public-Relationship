from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime
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
