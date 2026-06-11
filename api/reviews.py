from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from database.db import get_db
from database.schemas import ReviewCreate, ReviewResponse, UserResponse
from services import review_service


router = APIRouter()


@router.post("", response_model=ReviewResponse)
def create_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return review_service.create_review(db, current_user.id, review_data)


@router.get("", response_model=list[ReviewResponse])
def get_reviews(restaurant_id: Optional[int] = None, db: Session = Depends(get_db)):
    return review_service.get_reviews(db, restaurant_id)


@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    return review_service.get_review(db, review_id)


@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return review_service.delete_review(db, current_user.id, review_id)
