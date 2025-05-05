"""Модуль для работы с пользователями в базе данных (CRUD операции)."""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password, pwd_context


def get_user(db: Session, user_id: int):
    """Получение пользователя по ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Получение пользователя по email."""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: dict):
    """Создание нового пользователя с хешированием пароля."""
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Обновление данных пользователя."""
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.dict(exclude_unset=True)

        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Удаление пользователя."""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Аутентификация пользователя."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка соответствия пароля и его хеша."""
    return pwd_context.verify(plain_password, hashed_password)


def update_user_fitness_level(db: Session, user_id: int, new_level: str) -> Optional[User]:
    """Обновление уровня подготовки пользователя."""
    db_user = get_user(db, user_id)
    if db_user:
        db_user.fitness_level = new_level
        db.commit()
        db.refresh(db_user)
    return db_user


def get_users_by_fitness_goal(db: Session, goal: str, skip:
int = 0, limit: int = 100) -> list[User]:
    """Получение пользователей по цели тренировок."""
    return (
        db.query(User)
        .filter(User.fitness_goals.contains([goal]))
        .offset(skip)
        .limit(limit)
        .all()
    )
