"""Модуль содержит Pydantic-схемы для работы с пользователями."""

from typing import Optional, List, Union
from pydantic import BaseModel, EmailStr, Field  # Правильный импорт для Pydantic v1 и v2


class UserBase(BaseModel):
    """Базовая схема пользователя.

    Attributes:
        email (EmailStr): Электронная почта пользователя
        full_name (str, optional): Полное имя пользователя
        fitness_level (str, optional): Уровень подготовки
        age (int, optional): Возраст пользователя
        fitness_goals (List[str], optional): Список целей тренировок
    """
    email: EmailStr = Field("", example="user@example.com")
    full_name: str = Field("", example="Иван Иванов")


class UserCreate(BaseModel):
    email: EmailStr  # Автоматическая валидация email
    password: str
    full_name: Union[str, None] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
                "full_name": "John Doe"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr = Field("", example="user@example.com")
    password: str = Field("", example="securepassword123")

class UserOut(UserBase):
    id: int
    is_active: bool

class UserUpdate(UserBase):
    """Схема для обновления пользователя."""
    password: Optional[str] = None


class User(UserBase):
    """Основная схема пользователя (для чтения)."""
    id: int
    is_active: bool

    class Config:
        """Конфигурация Pydantic."""
        from_attributes = True  # Для Pydantic v2 используйте `from_attributes` вместо `orm_mode`