from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from database.db import get_db
from database.schemas import CartItemCreate, CartItemResponse, CartItemUpdate, CartResponse, UserResponse
from services import cart_service


router = APIRouter()


@router.post("/items", response_model=CartItemResponse)
def add_to_cart(
    cart_data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return cart_service.add_to_cart(db, current_user.id, cart_data)


@router.get("", response_model=CartResponse)
def get_cart(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return cart_service.get_cart(db, current_user.id)


@router.patch("/items/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(
    cart_item_id: int,
    cart_data: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return cart_service.update_cart_item(db, current_user.id, cart_item_id, cart_data)


@router.delete("/items/{cart_item_id}")
def delete_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return cart_service.delete_cart_item(db, current_user.id, cart_item_id)


@router.delete("/clear")
def clear_cart(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return cart_service.clear_cart(db, current_user.id)
