from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..models.Order import Order
from ..models.database import get_db


router = APIRouter()

@router.get('')
def index(jwt: str, db: Session = Depends(get_db)):
    orders = db.query(Order).where(Order.customer == 1)
    
    return 