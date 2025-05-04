from uuid import uuid4
from fastapi import status
from unittest.mock import patch

def test_user_sign_up(client):
    with patch("app.routers.auth.check_user_exits", return_value=False), \
         patch("app.routers.auth.add_user", return_value=None):
        
        response = client.post("/auth/sign-up", json={
            "email": "test@example.com",
            "password": "securepassword",
            "name": "Test User"
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"detail": "User created"}

def test_user_login_success(client):
    mock_user = type("User", (), {
        "uuid": uuid4(),
        "hashed_password": "hashed"
    })()

    with patch("app.routers.auth.check_user_exits", return_value=mock_user), \
         patch("app.routers.auth.verify_password", return_value=True), \
         patch("app.routers.auth.create_access_token", return_value="fake-jwt-token"):
        
        response = client.post("/auth/login", data={
            "username": "test@example.com",
            "password": "securepassword"
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "access_token": "fake-jwt-token",
            "token_type": "bearer"
        }
