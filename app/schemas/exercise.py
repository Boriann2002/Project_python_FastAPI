"""Модуль содержит Pydantic-схемы для работы с упражнениями."""

from typing import Optional
from pydantic import BaseModel


class ExerciseBase(BaseModel):
    """Базовая схема упражнения.

    Attributes:
        name (str): Название упражнения
        description (str, optional): Описание упражнения
        muscle_group (str): Группа мышц
        equipment (str): Необходимое оборудование
        difficulty (int): Уровень сложности (1-10)
        calories_burned (float): Количество сжигаемых калорий
        is_cardio (bool): Является ли кардио-упражнением
        avg_duration (int): Средняя продолжительность (в минутах)
    """
    name: str
    description: Optional[str] = None
    muscle_group: str
    equipment: str
    difficulty: int
    calories_burned: float
    is_cardio: bool
    avg_duration: int


class ExerciseCreate(ExerciseBase):
    """Схема для создания упражнения (наследует все поля ExerciseBase)."""



class ExerciseUpdate(ExerciseBase):
    """Схема для обновления упражнения (наследует все поля ExerciseBase)."""



class Exercise(ExerciseBase):
    """Основная схема упражнения (для чтения) с добавленным идентификатором.

    Attributes:
        id (int): Уникальный идентификатор упражнения
    """
    id: int

    class Config:  # pylint: disable=too-few-public-methods
        """Конфигурация Pydantic для работы с ORM."""
        from_attributes = True
