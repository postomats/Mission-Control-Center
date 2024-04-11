from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ..models.Order import Order, Basket, Cell
from ..models.database import get_db
from ..utilities import get_user_id_from_token, is_worker, open_cell, check_cell_status
router = APIRouter()


@router.get("/list")
def return_orders_by_user(jwt: str, db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(jwt)
    orders = [order.json() for order in (
        db.query(Order)
        .filter(Order.customer == user_id, Order.status != "closed")
        .all()
    )]
    return orders


@router.post("/do")
def create_order(
    jwt: str,
    content: str,
    db: Session = Depends(get_db),
):
    # Проверяем, что содержимое корзины передано
    if not content:
        raise HTTPException(status_code=400, detail="Требуется содержимое корзины.")

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
            raise HTTPException(status_code=404, detail="Заказ не найден.")
        if order.cell:
            raise HTTPException(status_code=409, detail="Заказ уже был обработан.")
        if not order.status == "created":
            raise HTTPException(status_code=409, detail=f"Заказ имеет статус {order.status}.")
        #TODO: брать MAX_CELL из INFO постоматов
        MAX_CELL = 24
        existing_cells = db.query(Cell.cell_id).all()
        existing_cells = {cell[0] for cell in existing_cells}
        #TODO: брать SERVICE_CELL из INFO постоматов
        SERVICE_CELL = 3
        existing_cells.add(SERVICE_CELL)
        missing_cells = [cell for cell in range(1, MAX_CELL + 1) if cell not in existing_cells]
        
        if missing_cells:
            unused_cell_id = min(missing_cells)
        else:
            HTTPException(status_code=503, detail="Извините, все ячейки в данный момент заняты. Пожалуйста, попробуйте позже.")
        new_cell = Cell(order_id=order_id, cell_id = unused_cell_id)
        db.add(new_cell)
        order.status = "processing"
        db.commit()
        return {"status": True}


@router.put("/{order_id}/reject")
def reject_order(jwt: str, order_id: int, db: Session = Depends(get_db)):
    if is_worker(jwt):
        # Получаем заказ из базы данных
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден.")
        if not order.status == "created":
            raise HTTPException(status_code=409, detail=f"Заказ имеет статус {order.status}.")
        new_cell = Cell(order_id=order_id, cell_id = None)
        db.add(new_cell)
        order.status = "rejected"
        db.commit()
        return {"status": True}


@router.put("/{order_id}/deliver")
def deliver_order(jwt: str, order_id: int, db: Session = Depends(get_db)):
    if is_worker(jwt):
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order.status == "processing":
            raise HTTPException(status_code=409, detail=f"Заказ имеет статус {order.status}.")
        cell_id = order.cell[0].cell_id
        open_cell(cell_id)
        if not check_cell_status(cell_id):
            raise HTTPException(status_code=403, detail="Не удалось открыть ячейку.")
        order.status = "delivered"
        db.commit()
        return {"status": True, "cell": cell_id}


@router.get("/{cell_id}/is_open")
def is_open_cell(cell_id: int):
    return {"status": check_cell_status(cell_id)}


@router.put("/{order_id}/receive")
def receive_order(jwt: str, order_id: int, db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(jwt)
    order = db.query(Order).filter(Order.id == order_id).first()
    if order.customer != user_id:
        raise HTTPException(status_code=403, detail="У вас нет разрешения на обработку этого заказа.")
    if not order.status == "delivered":
            raise HTTPException(status_code=409, detail=f"Заказ имеет статус {order.status}.")
    cell = order.cell[0]
    open_cell(cell.cell_id)
    opened_cell = cell.cell_id
    order.status = "received"
    cell.cell_id = None
    db.commit()
    return {"status": True, "cell": opened_cell}


@router.put("/{order_id}/return")
def return_order(jwt: str, order_id: int, db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(jwt)
    order = db.query(Order).filter(Order.id == order_id).first()
    if order.customer != user_id:
        raise HTTPException(status_code=403, detail="У вас нет разрешения на обработку этого заказа.")
    if not order.status == "received":
            raise HTTPException(status_code=409, detail=f"Заказ имеет статус {order.status}.")
    #TODO: брать MAX_CELL из INFO постоматов
    MAX_CELL = 24
    existing_cells = db.query(Cell.cell_id).all()
    existing_cells = {cell[0] for cell in existing_cells}
    #TODO: брать SERVICE_CELL из INFO постоматов
    SERVICE_CELL = 3
    existing_cells.add(SERVICE_CELL)
    missing_cells = [cell for cell in range(1, MAX_CELL + 1) if cell not in existing_cells]
    print(missing_cells)
    if missing_cells:
        unused_cell_id = min(missing_cells)
        print(unused_cell_id)   
    else:
        HTTPException(status_code=503, detail="Извините, все ячейки в данный момент заняты. Пожалуйста, попробуйте позже.")
    cell = order.cell[0]
    open_cell(unused_cell_id)
    cell.cell_id = unused_cell_id
    order.status = "returned"
    db.commit()
    return {"status": True, "cell": unused_cell_id}


@router.put("/{order_id}/take_back")
def take_back_order(jwt: str, order_id: int, db: Session = Depends(get_db)):
    if is_worker(jwt):
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order.status == "returned":
            raise HTTPException(status_code=409, detail=f"Заказ имеет статус {order.status}.")
        cell = order.cell[0]
        open_cell(cell.cell_id)
        opened_cell = cell.cell_id
        cell.cell_id = None
        order.status = "closed"
        db.commit()
        return {"status": True, "cell": opened_cell}


@router.get("/orders_list")
def return_orders_by_user(jwt: str, db: Session = Depends(get_db)):
    if is_worker(jwt):
        orders = [order.json() for order in (
            db.query(Order)
            .filter(Order.status !="closed", Order.status !="rejected", Order.status !="received")
            .all()
        )]
        return orders
    raise HTTPException(status_code=403, detail="Нет прав доступа для просмотра списка заказов") 