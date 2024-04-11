from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from ..models.Order import Order, Basket
from ..models.database import get_db
from ..utilities import get_user_id_from_token, is_worker

router = APIRouter()


@router.get("/list")
def return_orders_by_user(jwt: str, db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(jwt)
    orders = (
        db.query(Order)
        .filter(Order.customer == user_id, Order.status != "closed")
        .all()
    )
    return orders


@router.post("/do")
def create_order(
    jwt: str,
    content: dict = Body(...),
    db: Session = Depends(get_db),
):
    # Проверяем, что содержимое корзины передано
    if not content:
        raise HTTPException(status_code=400, detail="Basket content is required")

    # Получаем id пользователя из токена
    user_id = get_user_id_from_token(jwt)
    # Создаем новый заказ
    new_order = Order(customer=user_id, status="created")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Создаем запись в корзине для нового заказа
    new_basket = Basket(order_id=new_order.id, content=content)
    db.add(new_basket)
    db.commit()

    return {"status": True}


@router.put("/{order_id}/process")
def process_order(jwt: str, order_id: int, db: Session = Depends(get_db)):
    if is_worker(jwt):
        # Получаем заказ из базы данных
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order.status = "processing"
        db.commit()
        return {"status": True}


@router.put("/{order_id}/reject")
def reject_order(jwt: str, order_id: int, db: Session = Depends(get_db)):
    if is_worker(jwt):
        # Получаем заказ из базы данных
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order.status = "rejected"
        db.commit()
        return {"status": True}


@router.put("/{order_id}/deliver")
def deliver_order(jwt: str, order_id: int, db: Session = Depends(get_db)):
    pass


@router.put("/{order_id}/receive")
def receive_order(jwt: str, order_id: int, db: Session = Depends(get_db)):
    pass
    