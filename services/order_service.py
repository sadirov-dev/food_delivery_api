from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from database import models, schemas


VALID_ORDER_STATUSES = {
    models.OrderStatus.pending.value,
    models.OrderStatus.accepted.value,
    models.OrderStatus.cooking.value,
    models.OrderStatus.delivering.value,
    models.OrderStatus.completed.value,
    models.OrderStatus.cancelled.value,
}


def create_order(db: Session, user_id: int, order_data: schemas.OrderCreate):
    address = db.query(models.Address).filter(
        models.Address.id == order_data.address_id,
        models.Address.user_id == user_id,
    ).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    cart_items = (
        db.query(models.CartItem)
        .options(joinedload(models.CartItem.food).joinedload(models.Food.restaurant))
        .filter(models.CartItem.user_id == user_id)
        .all()
    )
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    unavailable_food = next((item for item in cart_items if not item.food.is_available), None)
    if unavailable_food:
        raise HTTPException(status_code=400, detail="Cart contains unavailable food")

    subtotal = sum(item.food.price * item.quantity for item in cart_items)
    delivery_price = max((item.food.restaurant.delivery_price for item in cart_items), default=0)

    order = models.Order(
        user_id=user_id,
        address_id=order_data.address_id,
        total_price=subtotal + delivery_price,
        delivery_price=delivery_price,
        payment_method=order_data.payment_method,
        status=models.OrderStatus.pending.value,
    )
    db.add(order)
    db.flush()

    for item in cart_items:
        order_item = models.OrderItem(
            order_id=order.id,
            food_id=item.food_id,
            quantity=item.quantity,
            price=item.food.price,
        )
        db.add(order_item)

    db.query(models.CartItem).filter(models.CartItem.user_id == user_id).delete()
    db.commit()
    db.refresh(order)
    return get_order(db, user_id, order.id)


def get_orders(db: Session, user_id: int):
    return (
        db.query(models.Order)
        .options(
            joinedload(models.Order.items).joinedload(models.OrderItem.food).joinedload(models.Food.restaurant),
            joinedload(models.Order.items).joinedload(models.OrderItem.food).joinedload(models.Food.category),
            joinedload(models.Order.address),
        )
        .filter(models.Order.user_id == user_id)
        .order_by(models.Order.created_at.desc())
        .all()
    )


def get_order(db: Session, user_id: int, order_id: int):
    order = (
        db.query(models.Order)
        .options(
            joinedload(models.Order.items).joinedload(models.OrderItem.food).joinedload(models.Food.restaurant),
            joinedload(models.Order.items).joinedload(models.OrderItem.food).joinedload(models.Food.category),
            joinedload(models.Order.address),
        )
        .filter(models.Order.id == order_id, models.Order.user_id == user_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def update_order_status(db: Session, user_id: int, order_id: int, status_data: schemas.OrderStatusUpdate):
    if status_data.status not in VALID_ORDER_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid order status")

    order = get_order(db, user_id, order_id)
    order.status = status_data.status
    db.commit()
    db.refresh(order)
    return get_order(db, user_id, order_id)
