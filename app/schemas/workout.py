"""Модуль содержит Pydantic-схемы для работы с тренировками и планами тренировок."""
from __future__ import annotations

from datetime import date
from typing import List, Optional, Any, Union
from pydantic import BaseModel, Field
from app.schemas.exercise import Exercise

class WorkoutBase(BaseModel):
    """Базовая схема тренировки.

    Attributes:
        name (str): Название тренировки
        date (date): Дата проведения тренировки
        duration (int): Продолжительность в минутах
        notes (str, optional): Дополнительные заметки
    """
    name: str = Field("", description="Название тренировки", example="Силовая тренировка")
    date: str = Field("", description="Дата тренировки", example="2023-12-15")
    duration: int = Field(0, description="Длительность в минутах", example=60, gt=0)
    notes: Union[Any, None] = Field(None, description="Дополнительные заметки", example="Тяжелая тренировка")

class WorkoutCreate(WorkoutBase):
    """Схема для создания тренировки.

    Attributes:
        exercise_ids (List[int]): Список ID упражнений
    """
    exercise_ids: Any = Field("", description="Список ID упражнений", example=[1, 2, 3])


class WorkoutUpdate(WorkoutBase):
    """Схема для обновления тренировки.

    Attributes:
        exercise_ids (List[int], optional): Список ID упражнений
    """
    name: Union[Any, None] = Field(None, description="Название тренировки", example="Кардио тренировка")
    duration: Union[Any, None] = Field(None, description="Длительность в минутах", example=45)
    notes: Any = Field(None, description="Дополнительные заметки")

class Workout(WorkoutBase):
    """Основная схема тренировки (для чтения).

    Attributes:
        id (int): Уникальный идентификатор тренировки
        owner_id (int): ID владельца тренировки
        exercises (List[Exercise]): Список упражнений
    """
    id: Any = Field("", description="ID тренировки", example=1)
    owner_id: Any = Field("", description="ID владельца", example=1)

    class Config:  # pylint: disable=too-few-public-methods
        """Конфигурация Pydantic для работы с ORM."""
        from_attributes = True


class WorkoutOptimizationParams(BaseModel):
    """Параметры для оптимизации тренировки.

    Attributes:
        goal (str): Цель тренировки (weight_loss/muscle_gain/endurance)
        available_time (int): Доступное время в минутах
        target_muscles (List[str]): Целевые группы мышц
    """
    goal: str  # weight_loss, muscle_gain, endurance
    available_time: int  # in minutes
    target_muscles: List[str] = []


class WorkoutPlan(BaseModel):
    """План тренировки.

    Attributes:
        exercises (List[dict]): Список упражнений
        total_duration (int): Общая продолжительность
        estimated_calories (float): Расчетные калории
        difficulty (float): Сложность тренировки
    """
    exercises: List[dict]  # или используйте конкретную схему Exercise
    total_duration: int
    estimated_calories: float
    difficulty: float
