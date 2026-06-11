from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import models, schemas


def _reset_default_addresses(db: Session, user_id: int):
    db.query(models.Address).filter(models.Address.user_id == user_id).update({"is_default": False})


def create_address(db: Session, user_id: int, address_data: schemas.AddressCreate):
    if address_data.is_default:
        _reset_default_addresses(db, user_id)

    address = models.Address(user_id=user_id, **address_data.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def get_addresses(db: Session, user_id: int):
    return db.query(models.Address).filter(models.Address.user_id == user_id).order_by(models.Address.created_at.desc()).all()


def get_address(db: Session, user_id: int, address_id: int):
    address = db.query(models.Address).filter(
        models.Address.id == address_id,
        models.Address.user_id == user_id,
    ).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


def update_address(db: Session, user_id: int, address_id: int, address_data: schemas.AddressUpdate):
    address = get_address(db, user_id, address_id)
    if address_data.is_default:
        _reset_default_addresses(db, user_id)

    for key, value in address_data.model_dump().items():
        setattr(address, key, value)
    db.commit()
    db.refresh(address)
    return address


def delete_address(db: Session, user_id: int, address_id: int):
    address = get_address(db, user_id, address_id)
    db.delete(address)
    db.commit()
    return {"message": "Address deleted"}
