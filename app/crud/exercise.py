"""Модуль для работы с упражнениями в базе данных (CRUD операции)."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.exercise import Exercise as models_Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate


def get_exercise(db: Session, exercise_id: int) -> Optional[models_Exercise]:
    """Получение одного упражнения по ID.

    Args:
        db: Сессия базы данных
        exercise_id: ID упражнения

    Returns:
        Объект упражнения или None, если не найдено
    """
    return db.query(models_Exercise).filter(models_Exercise.id == exercise_id).first()


def get_exercises(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
) -> List[models_Exercise]:
    """Получение списка упражнений с возможностью пагинации и поиска.

    Args:
        db: Сессия базы данных
        skip: Количество пропускаемых записей
        limit: Максимальное количество возвращаемых записей
        search: Строка для поиска по названию

    Returns:
        Список упражнений
    """
    query = db.query(models_Exercise)

    if search:
        query = query.filter(models_Exercise.name.ilike(f"%{search}%"))

    return query.offset(skip).limit(limit).all()


def create_exercise(db: Session, exercise: ExerciseCreate) -> models_Exercise:
    """Создание нового упражнения.

    Args:
        db: Сессия базы данных
        exercise: Данные для создания упражнения

    Returns:
        Созданное упражнение
    """
    db_exercise = models_Exercise(
        name=exercise.name,
        description=exercise.description,
        muscle_group=exercise.muscle_group,
        equipment=exercise.equipment,
        difficulty=exercise.difficulty,
        calories_burned=exercise.calories_burned,
        is_cardio=exercise.is_cardio,
        avg_duration=exercise.avg_duration
    )
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def update_exercise(
        db: Session,
        exercise_id: int,
        exercise_update: ExerciseUpdate
) -> Optional[models_Exercise]:
    """Обновление данных упражнения.

    Args:
        db: Сессия базы данных
        exercise_id: ID упражнения
        exercise_update: Новые данные упражнения

    Returns:
        Обновленное упражнение или None, если не найдено
    """
    db_exercise = get_exercise(db, exercise_id)
    if db_exercise:
        update_data = exercise_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_exercise, field, value)
        db.commit()
        db.refresh(db_exercise)
    return db_exercise


def delete_exercise(db: Session, exercise_id: int) -> bool:
    """Удаление упражнения.

    Args:
        db: Сессия базы данных
        exercise_id: ID упражнения

    Returns:
        True, если удаление прошло успешно, иначе False
    """
    db_exercise = get_exercise(db, exercise_id)
    if db_exercise:
        db.delete(db_exercise)
        db.commit()
        return True
    return False


def get_exercises_by_muscle_group(
        db: Session,
        muscle_group: str,
        skip: int = 0,
        limit: int = 100
) -> List[models_Exercise]:
    """Получение упражнений по группе мышц.

    Args:
        db: Сессия базы данных
        muscle_group: Группа мышц для фильтрации
        skip: Количество пропускаемых записей
        limit: Максимальное количество возвращаемых записей

    Returns:
        Список упражнений для указанной группы мышц
    """
    return (
        db.query(models_Exercise)
        .filter(models_Exercise.muscle_group == muscle_group)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_cardio_exercises(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[models_Exercise]:
    """Получение кардио упражнений.

    Args:
        db: Сессия базы данных
        skip: Количество пропускаемых записей
        limit: Максимальное количество возвращаемых записей

    Returns:
        Список кардио упражнений
    """
    return (
        db.query(models_Exercise)
        .filter(models_Exercise.is_cardio.is_(True))  # Исправлено сравнение
        .offset(skip)
        .limit(limit)
        .all()
    )
