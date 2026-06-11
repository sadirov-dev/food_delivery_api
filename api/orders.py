from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from database.db import get_db
from database.schemas import OrderCreate, OrderResponse, OrderStatusUpdate, UserResponse
from services import order_service


router = APIRouter()


@router.post("", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return order_service.create_order(db, current_user.id, order_data)


@router.get("", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return order_service.get_orders(db, current_user.id)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return order_service.get_order(db, current_user.id, order_id)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return order_service.update_order_status(db, current_user.id, order_id, status_data)
