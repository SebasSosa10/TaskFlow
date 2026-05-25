import pytest

from src.shared.exceptions.domain import ForbiddenError, NotFoundError
from tests.test_integration.conftest import SAMPLE_PROJECT


class TestCreateProjectEndpoint:
    async def test_create_project_success(
        self, authenticated_client, mock_project_service
    ):
        mock_project_service.create_project.return_value = SAMPLE_PROJECT

        response = await authenticated_client.post(
            "/api/projects",
            json={"name": "New Project", "owner_id": 1},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Sample Project"
        assert data["owner_id"] == 1
        assert data["status"] == "activo"

    async def test_create_project_owner_not_found(
        self, authenticated_client, mock_project_service
    ):
        mock_project_service.create_project.side_effect = NotFoundError(
            "Propietario con id 999 no encontrado"
        )

        response = await authenticated_client.post(
            "/api/projects",
            json={"name": "Project", "owner_id": 999},
        )

        assert response.status_code == 404
        assert "Propietario" in response.json()["detail"]

    async def test_create_project_forbidden(
        self, authenticated_client, mock_project_service
    ):
        mock_project_service.create_project.side_effect = ForbiddenError(
            "No tienes permisos"
        )

        response = await authenticated_client.post(
            "/api/projects",
            json={"name": "Project", "owner_id": 1},
        )

        assert response.status_code == 403

    async def test_create_project_missing_name(self, authenticated_client):
        response = await authenticated_client.post(
            "/api/projects",
            json={"owner_id": 1},
        )

        assert response.status_code == 422

    async def test_create_project_without_token(self, unauthenticated_client):
        response = await unauthenticated_client.post(
            "/api/projects",
            json={"name": "Project", "owner_id": 1},
        )

        assert response.status_code == 401


class TestListProjectsEndpoint:
    async def test_list_projects_success(
        self, authenticated_client, mock_project_service
    ):
        mock_project_service.get_projects.return_value = ([SAMPLE_PROJECT], 1)

        response = await authenticated_client.get("/api/projects")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Sample Project"

    async def test_list_projects_without_token(self, unauthenticated_client):
        response = await unauthenticated_client.get("/api/projects")

        assert response.status_code == 401
