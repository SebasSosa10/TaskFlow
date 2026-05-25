from src.modules.auth.schemas.auth import TokenResponse
from src.shared.exceptions.domain import AlreadyExistsError, UnauthorizedError
from tests.test_integration.conftest import REGULAR_USER


class TestLoginEndpoint:
    async def test_login_returns_token(self, authenticated_client, mock_auth_service):
        mock_auth_service.login.return_value = TokenResponse(
            access_token="jwt.token.here", token_type="bearer"
        )

        response = await authenticated_client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "password123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["access_token"] == "jwt.token.here"
        assert data["token_type"] == "bearer"

    async def test_login_invalid_credentials(
        self, authenticated_client, mock_auth_service
    ):
        mock_auth_service.login.side_effect = UnauthorizedError(
            "Credenciales inválidas"
        )

        response = await authenticated_client.post(
            "/api/auth/login",
            json={"username": "wronguser", "password": "wrongpass"},
        )

        assert response.status_code == 401
        assert "Credenciales inválidas" in response.json()["detail"]

    async def test_login_missing_fields(self, authenticated_client):
        response = await authenticated_client.post(
            "/api/auth/login",
            json={"username": "admin"},
        )

        assert response.status_code == 422


class TestRegisterEndpoint:
    async def test_register_success(self, authenticated_client, mock_auth_service):
        mock_auth_service.register.return_value = REGULAR_USER

        response = await authenticated_client.post(
            "/api/auth/register",
            json={
                "email": "user@taskflow.com",
                "username": "regularuser",
                "password": "password123",
                "full_name": "Regular User",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "user@taskflow.com"
        assert data["username"] == "regularuser"
        assert data["role"] == "usuario"

    async def test_register_email_already_exists(
        self, authenticated_client, mock_auth_service
    ):
        mock_auth_service.register.side_effect = AlreadyExistsError(
            "El email ya está registrado"
        )

        response = await authenticated_client.post(
            "/api/auth/register",
            json={
                "email": "existing@test.com",
                "username": "newuser",
                "password": "password123",
                "full_name": "Test User",
            },
        )

        assert response.status_code == 409
        assert "email ya está registrado" in response.json()["detail"]

    async def test_register_invalid_email(self, authenticated_client):
        response = await authenticated_client.post(
            "/api/auth/register",
            json={
                "email": "not-an-email",
                "username": "newuser",
                "password": "password123",
                "full_name": "Test",
            },
        )

        assert response.status_code == 422


class TestMeEndpoint:
    async def test_get_me_authenticated(self, authenticated_client):
        response = await authenticated_client.get("/api/auth/me")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["email"] == "admin@taskflow.com"
        assert data["role"] == "administrador"

    async def test_get_me_without_token(self, unauthenticated_client):
        response = await unauthenticated_client.get("/api/auth/me")

        assert response.status_code == 401
