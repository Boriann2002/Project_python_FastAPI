"""Модуль содержит модель упражнения (Exercise) для работы с базой данных."""

from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base # pylint: disable=import-error


class Exercise(Base):
    """Модель упражнения в системе.

    Attributes:
        id (int): Уникальный идентификатор упражнения.
        name (str): Название упражнения.
        description (str): Описание упражнения.
        muscle_group (str): Группа мышц (chest, back, legs и т.д.).
        equipment (str): Необходимое оборудование.
        difficulty (int): Сложность (по шкале 1-10).
        calories_burned (float): Количество сжигаемых калорий в минуту.
        is_cardio (bool): Является ли упражнение кардио.
        avg_duration (int): Средняя продолжительность (в минутах).
        workouts (relationship): Связь многие-ко-многим с тренировками.
    """

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    muscle_group = Column(String)  # chest, back, legs, etc.
    equipment = Column(String)
    difficulty = Column(Integer)  # 1-10 scale
    calories_burned = Column(Float)  # per minute
    is_cardio = Column(Boolean)
    avg_duration = Column(Integer)  # in minutes

    workouts = relationship("Workout", secondary="workout_exercise", back_populates="exercises")
