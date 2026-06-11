from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.schemas import FoodCreate, FoodResponse, FoodUpdate
from services import food_service


router = APIRouter()


@router.post("", response_model=FoodResponse)
def create_food(food_data: FoodCreate, db: Session = Depends(get_db)):
    return food_service.create_food(db, food_data)


@router.get("", response_model=list[FoodResponse])
def get_foods(
    search: Optional[str] = None,
    restaurant_id: Optional[int] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_popular: Optional[bool] = None,
    is_available: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    return food_service.get_foods(
        db=db,
        search=search,
        restaurant_id=restaurant_id,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        is_popular=is_popular,
        is_available=is_available,
    )


@router.get("/{food_id}", response_model=FoodResponse)
def get_food(food_id: int, db: Session = Depends(get_db)):
    return food_service.get_food(db, food_id)


@router.put("/{food_id}", response_model=FoodResponse)
def update_food(food_id: int, food_data: FoodUpdate, db: Session = Depends(get_db)):
    return food_service.update_food(db, food_id, food_data)


@router.delete("/{food_id}")
def delete_food(food_id: int, db: Session = Depends(get_db)):
    return food_service.delete_food(db, food_id)
