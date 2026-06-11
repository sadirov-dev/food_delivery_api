from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.schemas import RestaurantCreate, RestaurantResponse, RestaurantUpdate
from services import restaurant_service


router = APIRouter()


@router.post("", response_model=RestaurantResponse)
def create_restaurant(restaurant_data: RestaurantCreate, db: Session = Depends(get_db)):
    return restaurant_service.create_restaurant(db, restaurant_data)


@router.get("", response_model=list[RestaurantResponse])
def get_restaurants(db: Session = Depends(get_db)):
    return restaurant_service.get_restaurants(db)


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    return restaurant_service.get_restaurant(db, restaurant_id)


@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(restaurant_id: int, restaurant_data: RestaurantUpdate, db: Session = Depends(get_db)):
    return restaurant_service.update_restaurant(db, restaurant_id, restaurant_data)


@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    return restaurant_service.delete_restaurant(db, restaurant_id)
