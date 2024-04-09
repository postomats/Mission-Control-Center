from .database import Base, engine

from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, DateTime, Enum, JSON
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer = Column(Integer)
    status = Column(Enum('created', 'processing', 'devilery', 'done', 'closed', 'rejected', name="pgenum"))

    basket = relationship("Basket", back_populates="book")


class Basket(Base):
    __tablename__ = 'baskets'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    content = Column(JSON)

    book = relationship("Order", back_populates="basket")
    

Base.metadata.create_all(bind=engine)