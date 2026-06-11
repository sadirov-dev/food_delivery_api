from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from database import models, schemas


def add_to_cart(db: Session, user_id: int, cart_data: schemas.CartItemCreate):
    food = db.query(models.Food).filter(models.Food.id == cart_data.food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    if not food.is_available:
        raise HTTPException(status_code=400, detail="Food is unavailable")

    cart_item = (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == user_id, models.CartItem.food_id == cart_data.food_id)
        .first()
    )
    if cart_item:
        cart_item.quantity += cart_data.quantity
    else:
        cart_item = models.CartItem(user_id=user_id, **cart_data.model_dump())
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item


def get_cart(db: Session, user_id: int):
    items = (
        db.query(models.CartItem)
        .options(
            joinedload(models.CartItem.food).joinedload(models.Food.restaurant),
            joinedload(models.CartItem.food).joinedload(models.Food.category),
        )
        .filter(models.CartItem.user_id == user_id)
        .order_by(models.CartItem.created_at.desc())
        .all()
    )
    subtotal = sum(item.food.price * item.quantity for item in items)
    total_items = sum(item.quantity for item in items)
    return {"items": items, "subtotal": subtotal, "total_items": total_items}


def update_cart_item(db: Session, user_id: int, cart_item_id: int, cart_data: schemas.CartItemUpdate):
    cart_item = (
        db.query(models.CartItem)
        .options(joinedload(models.CartItem.food))
        .filter(models.CartItem.id == cart_item_id, models.CartItem.user_id == user_id)
        .first()
    )
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if not cart_item.food.is_available:
        raise HTTPException(status_code=400, detail="Food is unavailable")

    cart_item.quantity = cart_data.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


def delete_cart_item(db: Session, user_id: int, cart_item_id: int):
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == cart_item_id,
        models.CartItem.user_id == user_id,
    ).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"message": "Cart item deleted"}


def clear_cart(db: Session, user_id: int):
    db.query(models.CartItem).filter(models.CartItem.user_id == user_id).delete()
    db.commit()
    return {"message": "Cart cleared"}
