from fastapi.testclient import TestClient


DEFAULT_USERNAME = "apiuser"
DEFAULT_EMAIL = "api@example.com"
DEFAULT_PASSWORD = "strongpassword123"


def register_user(
    client: TestClient,
    username: str = DEFAULT_USERNAME,
    email: str = DEFAULT_EMAIL,
    password: str = DEFAULT_PASSWORD,
):
    return client.post(
        "/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )


def login_user(
    client: TestClient,
    username: str = DEFAULT_USERNAME,
    password: str = DEFAULT_PASSWORD,
):
    return client.post(
        "/login",
        json={
            "username": username,
            "password": password,
        },
    )


def authorization_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_register_creates_new_user(client: TestClient):
    response = register_user(client)

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"


def test_register_rejects_duplicate_username(client: TestClient):
    register_user(client)

    response = register_user(
        client,
        email="another@example.com",
    )

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_login_returns_access_token_for_valid_credentials(client: TestClient):
    register_user(client)

    response = login_user(client)

    assert response.status_code == 200

    body = response.json()

    assert body["access_token"]
    assert body["token_type"] == "bearer"


def test_login_rejects_invalid_password(client: TestClient):
    register_user(client)

    response = login_user(
        client,
        password="incorrect-password",
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_login_rejects_unknown_user(client: TestClient):
    response = login_user(
        client,
        username="unknown-user",
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_authenticated_user_can_fetch_profile(client: TestClient):
    register_user(client)

    login_response = login_user(client)
    token = login_response.json()["access_token"]

    response = client.get(
        "/me",
        headers=authorization_header(token),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["username"] == DEFAULT_USERNAME
    assert body["email"] == DEFAULT_EMAIL


def test_profile_endpoint_requires_authentication(client: TestClient):
    response = client.get("/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing or invalid authorization header"


def test_profile_endpoint_rejects_invalid_token(client: TestClient):
    response = client.get(
        "/me",
        headers=authorization_header("invalid.jwt.token"),
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"