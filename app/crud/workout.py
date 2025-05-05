"""Модуль для работы с тренировками в базе данных (CRUD операции)."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.workout import Workout as models_Workout
from app.schemas.workout import WorkoutCreate, WorkoutUpdate


def create_workout(db: Session, workout: WorkoutCreate, user_id: int) -> models_Workout:
    """Создание новой тренировки для пользователя.

    Args:
        db: Сессия базы данных
        workout: Данные для создания тренировки
        user_id: ID владельца тренировки

    Returns:
        Созданная тренировка
    """
    db_workout = models_Workout(
        **workout.dict(),
        owner_id=user_id
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


def get_workout(db: Session, workout_id: int) -> Optional[models_Workout]:
    """Получение тренировки по ID.

    Args:
        db: Сессия базы данных
        workout_id: ID тренировки

    Returns:
        Найденная тренировка или None
    """
    return db.query(models_Workout).filter(models_Workout.id == workout_id).first()


def get_workouts(
        db: Session,
        owner_id: int,
        filters: Optional[dict] = None,
        pagination: Optional[dict] = None
) -> List[models_Workout]:
    """Получение списка тренировок пользователя с фильтрами и пагинацией.

    Args:
        db: Сессия базы данных
        owner_id: ID владельца тренировок
        filters: Словарь с фильтрами (может содержать start_date, end_date)
        pagination: Словарь с параметрами пагинации (skip, limit)

    Returns:
        Список тренировок
    """
    # Устанавливаем значения по умолчанию
    filters = filters or {}
    pagination = pagination or {}

    query = db.query(models_Workout).filter(models_Workout.owner_id == owner_id)

    if 'start_date' in filters:
        query = query.filter(models_Workout.date >= filters['start_date'])
    if 'end_date' in filters:
        query = query.filter(models_Workout.date <= filters['end_date'])

    skip = pagination.get('skip', 0)
    limit = pagination.get('limit', 100)

    return query.offset(skip).limit(limit).all()

def update_workout(
        db: Session,
        workout_id: int,
        workout_update: WorkoutUpdate
) -> Optional[models_Workout]:
    """Обновление данных тренировки.

    Args:
        db: Сессия базы данных
        workout_id: ID тренировки
        workout_update: Новые данные тренировки

    Returns:
        Обновленная тренировка или None
    """
    db_workout = get_workout(db, workout_id)
    if db_workout:
        update_data = workout_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_workout, field, value)
        db.commit()
        db.refresh(db_workout)
    return db_workout


def delete_workout(db: Session, workout_id: int) -> bool:
    """Удаление тренировки.

    Args:
        db: Сессия базы данных
        workout_id: ID тренировки

    Returns:
        True если удаление прошло успешно, иначе False
    """
    db_workout = get_workout(db, workout_id)
    if db_workout:
        db.delete(db_workout)
        db.commit()
        return True
    return False


def get_workouts_by_exercise(
        db: Session,
        exercise_id: int,
        owner_id: int,
        skip: int = 0,
        limit: int = 100
) -> List[models_Workout]:
    """Получение тренировок, содержащих указанное упражнение.

    Args:
        db: Сессия базы данных
        exercise_id: ID упражнения
        owner_id: ID владельца тренировок
        skip: Количество пропускаемых записей
        limit: Максимальное количество возвращаемых записей

    Returns:
        Список тренировок
    """
    return (
        db.query(models_Workout)
        .filter(models_Workout.owner_id == owner_id)
        .filter(models_Workout.exercises.any(id=exercise_id))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user_workout(db: Session, workout: WorkoutCreate, user_id: int) -> models_Workout:
    """Создание тренировки для пользователя (альтернативная реализация).

    Args:
        db: Сессия базы данных
        workout: Данные для создания тренировки
        user_id: ID владельца тренировки

    Returns:
        Созданная тренировка
    """
    db_workout = models_Workout(**workout.dict(), owner_id=user_id)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout
