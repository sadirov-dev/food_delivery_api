from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import models, schemas


def create_category(db: Session, category_data: schemas.CategoryCreate):
    existing_category = db.query(models.Category).filter(models.Category.title == category_data.title).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    category = models.Category(**category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session):
    return db.query(models.Category).order_by(models.Category.created_at.desc()).all()


def get_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def update_category(db: Session, category_id: int, category_data: schemas.CategoryUpdate):
    category = get_category(db, category_id)
    for key, value in category_data.model_dump().items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)
    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}
