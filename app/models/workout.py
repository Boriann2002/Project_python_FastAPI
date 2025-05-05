"""Модуль содержит модель тренировки (Workout) и ассоциативную таблицу для связи с упражнениями."""

from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base  # pylint: disable=import-error


class Workout(Base):
    """Модель тренировки в системе.

    Attributes:
        id (int): Уникальный идентификатор тренировки
        name (str): Название тренировки
        date (Date): Дата проведения тренировки
        duration (int): Продолжительность в минутах
        notes (str): Дополнительные заметки
        owner_id (int): ID владельца тренировки (связь с пользователем)
        exercises (relationship): Связь многие-ко-многим с упражнениями
    """

    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(Date)
    duration = Column(Integer)  # in minutes
    notes = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    exercises = relationship("Exercise", secondary="workout_exercise", back_populates="workouts")


# Association table for many-to-many relationship
workout_exercise = Table(
    'workout_exercise',
    Base.metadata,
    Column('workout_id', Integer, ForeignKey('workouts.id'), primary_key=True),
    Column('exercise_id', Integer, ForeignKey('exercises.id'), primary_key=True)
)

