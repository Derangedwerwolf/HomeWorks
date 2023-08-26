from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from api.schemas.contact import ContactResponse
from database.db import get_db
from database.crud import get_upcoming_birthdays

router = APIRouter(prefix="/birthdays", tags=["birthdays"])


@router.get("/", response_model=List[ContactResponse])
def get_upcoming_birthdays_list(days: int = 7, db: Session = Depends(get_db)):
    try:
        today = datetime.today().date()
        end_date = today + timedelta(days=days)
        return get_upcoming_birthdays(db=db, start_date=today, end_date=end_date)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
