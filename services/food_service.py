from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from database import models, schemas


def create_food(db: Session, food_data: schemas.FoodCreate):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == food_data.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    if food_data.category_id:
        category = db.query(models.Category).filter(models.Category.id == food_data.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    food = models.Food(**food_data.model_dump())
    db.add(food)
    db.commit()
    db.refresh(food)
    return food


def get_foods(
    db: Session,
    search: Optional[str] = None,
    restaurant_id: Optional[int] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_popular: Optional[bool] = None,
    is_available: Optional[bool] = None,
):
    query = db.query(models.Food).options(
        joinedload(models.Food.restaurant),
        joinedload(models.Food.category),
    )

    if search:
        query = query.filter(models.Food.title.ilike(f"%{search}%"))
    if restaurant_id:
        query = query.filter(models.Food.restaurant_id == restaurant_id)
    if category_id:
        query = query.filter(models.Food.category_id == category_id)
    if min_price is not None:
        query = query.filter(models.Food.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Food.price <= max_price)
    if is_popular is not None:
        query = query.filter(models.Food.is_popular == is_popular)
    if is_available is not None:
        query = query.filter(models.Food.is_available == is_available)

    return query.order_by(models.Food.created_at.desc()).all()


def get_food(db: Session, food_id: int):
    food = (
        db.query(models.Food)
        .options(joinedload(models.Food.restaurant), joinedload(models.Food.category))
        .filter(models.Food.id == food_id)
        .first()
    )
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


def update_food(db: Session, food_id: int, food_data: schemas.FoodUpdate):
    food = get_food(db, food_id)

    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == food_data.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    if food_data.category_id:
        category = db.query(models.Category).filter(models.Category.id == food_data.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    for key, value in food_data.model_dump().items():
        setattr(food, key, value)
    db.commit()
    db.refresh(food)
    return food


def delete_food(db: Session, food_id: int):
    food = get_food(db, food_id)
    db.delete(food)
    db.commit()
    return {"message": "Food deleted"}
