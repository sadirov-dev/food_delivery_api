from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import models, schemas


def create_review(db: Session, user_id: int, review_data: schemas.ReviewCreate):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == review_data.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    review = models.Review(user_id=user_id, **review_data.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)

    _update_restaurant_rating(db, review.restaurant_id)
    return review


def get_reviews(db: Session, restaurant_id: Optional[int] = None):
    query = db.query(models.Review)
    if restaurant_id:
        query = query.filter(models.Review.restaurant_id == restaurant_id)
    return query.order_by(models.Review.created_at.desc()).all()


def get_review(db: Session, review_id: int):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


def delete_review(db: Session, user_id: int, review_id: int):
    review = db.query(models.Review).filter(
        models.Review.id == review_id,
        models.Review.user_id == user_id,
    ).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    restaurant_id = review.restaurant_id
    db.delete(review)
    db.commit()
    _update_restaurant_rating(db, restaurant_id)
    return {"message": "Review deleted"}


def _update_restaurant_rating(db: Session, restaurant_id: int):
    reviews = db.query(models.Review).filter(models.Review.restaurant_id == restaurant_id).all()
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if restaurant:
        restaurant.rating = round(sum(review.rating for review in reviews) / len(reviews), 1) if reviews else 0
        db.commit()
