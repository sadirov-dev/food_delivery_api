from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.schemas import HomeResponse
from services.home_service import get_home_data


router = APIRouter()


@router.get("", response_model=HomeResponse)
def home(db: Session = Depends(get_db)):
    return get_home_data(db)
