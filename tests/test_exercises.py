from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models import exercise as models

client = TestClient(app)


def test_create_exercise(db: Session):
    exercise_data = {
        "name": "Push-up",
        "muscle_group": "chest",
        "equipment": "none",
        "difficulty": 3,
        "calories_burned": 5.0,
        "is_cardio": False,
        "avg_duration": 10
    }

    response = client.post(
        "/exercises/",
        json=exercise_data,
        headers={"Authorization": "Bearer valid_token"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Push-up"
    assert "id" in response.json()


def test_get_exercises(db: Session):
    # Create test exercise first
    db_exercise = models.Exercise(
        name="Test Exercise",
        muscle_group="back",
        equipment="none",
        difficulty=5,
        calories_burned=7.0,
        is_cardio=False,
        avg_duration=15
    )
    db.add(db_exercise)
    db.commit()

    response = client.get("/exercises/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any(ex["name"] == "Test Exercise" for ex in response.json())