"""Модуль содержит модель пользователя (User) для работы с базой данных."""

from sqlalchemy import Column, Integer, String, Boolean, ARRAY
from app.db.session import Base  # pylint: disable=import-error
from sqlalchemy import Table

from app.core.database import Base

"""Модель пользователя в системе.

    Attributes:
        id (int): Уникальный идентификатор пользователя.
        email (str): Электронная почта (уникальная).
        hashed_password (str): Хэшированный пароль.
        full_name (str): Полное имя пользователя.
        fitness_level (str): Уровень подготовки (beginner/intermediate/advanced).
        age (int): Возраст пользователя.
        fitness_goals (list[str]): Цели тренировок (weight_loss/muscle_gain/endurance).
        is_active (bool): Флаг активности пользователя.
    """
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"