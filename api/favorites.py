from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from database.db import get_db
from database.schemas import FavoriteResponse, UserResponse
from services import favorite_service


router = APIRouter()


@router.post("/{food_id}", response_model=FavoriteResponse)
def add_favorite(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return favorite_service.add_favorite(db, current_user.id, food_id)


@router.get("", response_model=list[FavoriteResponse])
def get_favorites(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return favorite_service.get_favorites(db, current_user.id)


@router.delete("/{food_id}")
def delete_favorite(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return favorite_service.delete_favorite(db, current_user.id, food_id)
