from .database import Base, engine
import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, DateTime, Enum, JSON
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = 'orders'
    created_date: datetime.datetime = Column(DateTime, default= datetime.datetime.now())
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer = Column(Integer)
    status = Column(Enum('created', 'processing', 'done', 'closed', 'rejected', name="pgenum"))

    basket = relationship("Basket", back_populates="order")


class Basket(Base):
    __tablename__ = 'baskets'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    content = Column(JSON)

    order = relationship("Order", back_populates="basket")
    

Base.metadata.create_all(bind=engine)