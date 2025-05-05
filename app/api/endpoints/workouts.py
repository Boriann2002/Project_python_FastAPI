from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app import models, schemas
from app.schemas.workout import Workout, WorkoutCreate

router = APIRouter()  # Это обязательная строка!

@router.post("/", response_model=Workout)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    db_workout = Workout(**workout.dict())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

@router.get("/", response_model=list[Workout])
def read_workouts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Workout).offset(skip).limit(limit).all()