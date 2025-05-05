from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models import user as models
from app.schemas import user as schemas

client = TestClient(app)


def test_create_user(db: Session):
    # Clean up test user if exists
    db.query(models.User).filter(models.User.email == "test@example.com").delete()
    db.commit()

    user_data = {
        "email": "test@example.com",
        "password": "testpass",
        "full_name": "Test User",
        "fitness_level": "beginner"
    }

    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert "id" in response.json()


def test_login(db: Session):
    # Ensure test user exists
    if not db.query(models.User).filter(models.User.email == "test@example.com").first():
        test_create_user(db)

    login_data = {
        "username": "test@example.com",
        "password": "testpass"
    }

    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()