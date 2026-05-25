import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app


class TestAuthProtection:
    """Verifica que los endpoints protegidos rechacen acceso sin token o con token inválido."""

    PROTECTED_ENDPOINTS = [
        ("GET", "/api/auth/me"),
        ("GET", "/api/users"),
        ("GET", "/api/projects"),
        ("GET", "/api/tasks"),
        ("GET", "/api/history"),
        ("GET", "/api/notifications"),
        ("GET", "/api/kanban/1"),
    ]

    @pytest.fixture(autouse=True)
    async def _clear_overrides(self):
        app.dependency_overrides.clear()
        yield
        app.dependency_overrides.clear()

    async def _make_client(self):
        transport = ASGITransport(app=app)
        return AsyncClient(transport=transport, base_url="http://test")

    async def test_no_token_returns_401(self):
        async with await self._make_client() as client:
            for method, path in self.PROTECTED_ENDPOINTS:
                response = await client.request(method, path)
                assert response.status_code == 401, (
                    f"{method} {path} debería retornar 401 sin token, "
                    f"pero retornó {response.status_code}"
                )

    async def test_invalid_token_returns_401(self):
        headers = {"Authorization": "Bearer token.invalido.aqui"}
        async with await self._make_client() as client:
            for method, path in self.PROTECTED_ENDPOINTS:
                response = await client.request(method, path, headers=headers)
                assert response.status_code == 401, (
                    f"{method} {path} debería retornar 401 con token inválido, "
                    f"pero retornó {response.status_code}"
                )

    async def test_malformed_auth_header_returns_401(self):
        headers = {"Authorization": "NotBearer some_token"}
        async with await self._make_client() as client:
            response = await client.get("/api/auth/me", headers=headers)
            assert response.status_code == 401

    async def test_health_is_public(self):
        async with await self._make_client() as client:
            response = await client.get("/health")
            assert response.status_code == 200
            assert response.json()["status"] == "ok"
