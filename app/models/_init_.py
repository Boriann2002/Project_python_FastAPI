from app.models.base import Base  # Или из файла, где объявлен Base
from app.models.user import User  # Импортируйте все модели
from app.models.exercise import Exercise
from app.models.workout import Workout

__all__ = ["Base", "User", "Exercise", "Workout"]