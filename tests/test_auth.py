from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import SessionLocal
from app.models.user import User as DBUser
from app.schemas.user import UserCreate

client = TestClient(app)


def test_create_user():
    db = SessionLocal()
    # Удаляем тестового пользователя если он существует
    db.query(DBUser).filter(DBUser.email == "test@example.com").delete()
    db.commit()

    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "testpass"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert "id" in response.json()


def test_login_for_token():
    response = client.post(
        "/auth/token",
        data={"username": "test@example.com", "password": "testpass"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_read_users_me():
    # Сначала получаем токен
    token_response = client.post(
        "/auth/token",
        data={"username": "test@example.com", "password": "testpass"},
    )
    token = token_response.json()["access_token"]

    # Затем используем токен для доступа к защищенному эндпоинту
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"