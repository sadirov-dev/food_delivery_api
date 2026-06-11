from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import models, schemas


def create_restaurant(db: Session, restaurant_data: schemas.RestaurantCreate):
    restaurant = models.Restaurant(**restaurant_data.model_dump())
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def get_restaurants(db: Session):
    return db.query(models.Restaurant).order_by(models.Restaurant.created_at.desc()).all()


def get_restaurant(db: Session, restaurant_id: int):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


def update_restaurant(db: Session, restaurant_id: int, restaurant_data: schemas.RestaurantUpdate):
    restaurant = get_restaurant(db, restaurant_id)
    for key, value in restaurant_data.model_dump().items():
        setattr(restaurant, key, value)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def delete_restaurant(db: Session, restaurant_id: int):
    restaurant = get_restaurant(db, restaurant_id)
    db.delete(restaurant)
    db.commit()
    return {"message": "Restaurant deleted"}
