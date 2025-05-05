from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Реализация регистрации
    pass