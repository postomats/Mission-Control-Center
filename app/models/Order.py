from .database import Base, engine
import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    ForeignKey,
    DateTime,
    Enum,
    JSON,
)
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = "orders"
    created_date = Column(DateTime, default=datetime.datetime.now())
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer = Column(Integer)
    status = Column(
        Enum(
            "created",
            "processing",
            "delivered",
            "received",
            "returned",
            "closed",
            "rejected",
            name="pgenum",
        )
    )
    cell = relationship("Cell", back_populates="order")
    basket = relationship("Basket", back_populates="order")

    def json(self):
        """
        Преобразует объект Order в словарь.

        :return: Словарь с данными объекта User.
        """
        return {
            "created": self.created_date,
            "status": self.status,
            "basket": self.basket[0].content,
        }


class Basket(Base):
    __tablename__ = "baskets"

    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    content = Column(JSON)

    order = relationship("Order", back_populates="basket")


class Cell(Base):
    __tablename__ = "cells"
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    cell_id = Column(Integer, default=None)
    order = relationship("Order", back_populates="cell")


Base.metadata.create_all(bind=engine)
