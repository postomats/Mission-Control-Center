from enum import Enum
from pydantic import BaseModel


class StatusCode(BaseModel):
    code: int
    status: str


class OrderStatusTypes(str, Enum):
    created = 'created'
    processing = 'processing'    
    done = 'done'
    closed = 'closed'
    rejected = 'rejected'


class Order(BaseModel):
    id: int
    customer: int
    status: OrderStatusTypes
    
    class Config:
        orm_mode = True
    
    
class Basket(BaseModel):
    order_id: int
    content: list
    
    
class BookBase(BaseModel):
    title: str
    author: str
    publication_year: int
    publisher: str