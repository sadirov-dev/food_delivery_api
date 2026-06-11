from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from database import models


def add_favorite(db: Session, user_id: int, food_id: int):
    food = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    favorite = db.query(models.Favorite).filter(
        models.Favorite.user_id == user_id,
        models.Favorite.food_id == food_id,
    ).first()
    if favorite:
        raise HTTPException(status_code=400, detail="Food already in favorites")

    favorite = models.Favorite(user_id=user_id, food_id=food_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite


def get_favorites(db: Session, user_id: int):
    return (
        db.query(models.Favorite)
        .options(
            joinedload(models.Favorite.food).joinedload(models.Food.restaurant),
            joinedload(models.Favorite.food).joinedload(models.Food.category),
        )
        .filter(models.Favorite.user_id == user_id)
        .order_by(models.Favorite.created_at.desc())
        .all()
    )


def delete_favorite(db: Session, user_id: int, food_id: int):
    favorite = db.query(models.Favorite).filter(
        models.Favorite.user_id == user_id,
        models.Favorite.food_id == food_id,
    ).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(favorite)
    db.commit()
    return {"message": "Favorite deleted"}
