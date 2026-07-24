
def test_register_creates_user(client):
    response = client.post(
        "/register",
        json={"username": "testuser", "email": "test@example.com", "password": "strongpassword123"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"


def test_register_duplicate_username_returns_409(client):
    client.post(
        "/register",
        json={"username": "testuser", "email": "test1@example.com", "password": "strongpassword123"},
    )
    response = client.post(
        "/register",
        json={"username": "testuser", "email": "test2@example.com", "password": "anotherpassword"},
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]