from fastapi.testclient import TestClient
from datetime import date
from sqlalchemy.orm import Session

from app.main import app
from app.models import workout as models, exercise as exercise_models

client = TestClient(app)


def test_create_workout(db: Session):
    # Create test exercise first
    db_exercise = exercise_models.Exercise(
        name="Test Exercise",
        muscle_group="legs",
        equipment="none",
        difficulty=4,
        calories_burned=6.0,
        is_cardio=False,
        avg_duration=12
    )
    db.add(db_exercise)
    db.commit()

    workout_data = {
        "name": "Morning Workout",
        "date": str(date.today()),
        "duration": 45,
        "exercise_ids": [db_exercise.id]
    }

    response = client.post(
        "/workouts/",
        json=workout_data,
        headers={"Authorization": "Bearer valid_token"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Morning Workout"
    assert len(response.json()["exercises"]) == 1