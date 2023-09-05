from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session


from app.main import app
from database.db import get_db

client = TestClient(app)


@patch("services.auth_manager")
def test_login_success(mock_auth_manager, db: Session):
    mock_auth_manager.verify_password.return_value = True

    login_data = {"username": "testuser", "password": "testpassword"}

    response = client.post("/login", data=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()


@patch("services.auth_manager")
def test_login_invalid_credentials(mock_auth_manager):
    mock_auth_manager.verify_password.return_value = False

    invalid_login_data = {"username": "testuser", "password": "invalidpassword"}

    response = client.post("/login", data=invalid_login_data)

    assert response.status_code == 401
    assert "detail" in response.json()


@patch("services.auth_manager")
def test_login_missing_fields():
    response = client.post("/login", data={})

    assert response.status_code == 422
    assert "username" in response.text
    assert "password" in response.text
