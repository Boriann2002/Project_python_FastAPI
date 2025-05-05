"""
Main FastAPI application module.
Defines the FastAPI app instance and connects all components.
"""
from datetime import date
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.db.base import Base, engine
from app.auth.auth import (
    get_current_user,
    create_access_token,
    authenticate_user,
    get_password_hash
)
from app.routers import auth_router
from app.core.security import get_password_hash, verify_password
from sqlalchemy.future import select
from .database import create_tables
from .routers import auth_router  # Импортируем роутер из отдельного файла


app = FastAPI(
    title="Fitness API",
    version="1.0.0",
    description="API for fitness workout tracking and optimization"
)

# Инициализация БД
@app.on_event("startup")
async def startup():
    await create_tables()

# Подключаем роутеры
app.include_router(auth_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

# Database initialization
from app.db.base import Base, engine

async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def startup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await startup_db()  # Не забываем await!


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Auth endpoints
@app.post(
    "/auth/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"]
)
async def register_user(
        user: UserCreate,
        db: Session = Depends(get_db)
):
    """Register a new user"""
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post(
    "/auth/login",
    response_model=Token,
    tags=["Authentication"]
)
@router.post("/login")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    # 1. Находим пользователя
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    # 2. Проверяем пароль
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Создаём токен
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}

# User endpoints
@app.get(
    "/users/me",
    response_model=UserOut,
    tags=["Users"]
)
async def read_current_user(
        current_user: User = Depends(get_current_user)
):
    """Get current authenticated user info"""
    return current_user


# Health check endpoints
@app.get("/", tags=["Root"])
async def root():
    """API health check"""
    return {
        "message": "Fitness API is running",
        "docs": "http://localhost:8000/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Service health monitoring"""
    return {"status": "healthy"}

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    @app.on_event("startup")
    async def startup():
        await init_models()
