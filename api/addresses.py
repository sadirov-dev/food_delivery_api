from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from database.db import get_db
from database.schemas import AddressCreate, AddressResponse, AddressUpdate, UserResponse
from services import address_service


router = APIRouter()


@router.post("", response_model=AddressResponse)
def create_address(
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return address_service.create_address(db, current_user.id, address_data)


@router.get("", response_model=list[AddressResponse])
def get_addresses(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return address_service.get_addresses(db, current_user.id)


@router.get("/{address_id}", response_model=AddressResponse)
def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return address_service.get_address(db, current_user.id, address_id)


@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    address_data: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return address_service.update_address(db, current_user.id, address_id, address_data)


@router.delete("/{address_id}")
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return address_service.delete_address(db, current_user.id, address_id)
