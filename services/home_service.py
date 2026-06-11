from sqlalchemy.orm import Session, joinedload

from database import models


def get_home_data(db: Session):
    categories = db.query(models.Category).order_by(models.Category.created_at.desc()).limit(8).all()
    popular_foods = (
        db.query(models.Food)
        .options(joinedload(models.Food.restaurant), joinedload(models.Food.category))
        .filter(models.Food.is_popular == True, models.Food.is_available == True)
        .order_by(models.Food.rating.desc(), models.Food.created_at.desc())
        .limit(8)
        .all()
    )
    open_restaurants = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.is_open == True)
        .order_by(models.Restaurant.rating.desc(), models.Restaurant.created_at.desc())
        .limit(8)
        .all()
    )
    recommended_foods = (
        db.query(models.Food)
        .options(joinedload(models.Food.restaurant), joinedload(models.Food.category))
        .filter(models.Food.is_available == True)
        .order_by(models.Food.rating.desc(), models.Food.created_at.desc())
        .limit(8)
        .all()
    )
    return {
        "categories": categories,
        "popular_foods": popular_foods,
        "open_restaurants": open_restaurants,
        "recommended_foods": recommended_foods,
    }
