from src.shared.exceptions.domain import ForbiddenError, NotFoundError
from tests.test_integration.conftest import SAMPLE_TASK


class TestCreateTaskEndpoint:
    async def test_create_task_success(self, authenticated_client, mock_task_service):
        mock_task_service.create_task.return_value = SAMPLE_TASK

        response = await authenticated_client.post(
            "/api/tasks",
            json={"title": "New Task", "project_id": 1, "priority": 2},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Sample Task"
        assert data["project_id"] == 1

    async def test_create_task_project_not_found(
        self, authenticated_client, mock_task_service
    ):
        mock_task_service.create_task.side_effect = NotFoundError(
            "Proyecto con id 999 no encontrado"
        )

        response = await authenticated_client.post(
            "/api/tasks",
            json={"title": "Task", "project_id": 999},
        )

        assert response.status_code == 404
        assert "Proyecto" in response.json()["detail"]

    async def test_create_task_forbidden(self, authenticated_client, mock_task_service):
        mock_task_service.create_task.side_effect = ForbiddenError("No tienes permisos")

        response = await authenticated_client.post(
            "/api/tasks",
            json={"title": "Task", "project_id": 1},
        )

        assert response.status_code == 403

    async def test_create_task_missing_title(self, authenticated_client):
        response = await authenticated_client.post(
            "/api/tasks",
            json={"project_id": 1},
        )

        assert response.status_code == 422

    async def test_create_task_without_token(self, unauthenticated_client):
        response = await unauthenticated_client.post(
            "/api/tasks",
            json={"title": "Task", "project_id": 1},
        )

        assert response.status_code == 401


class TestListTasksEndpoint:
    async def test_list_tasks_success(self, authenticated_client, mock_task_service):
        mock_task_service.get_tasks.return_value = ([SAMPLE_TASK], 1)

        response = await authenticated_client.get("/api/tasks")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "Sample Task"

    async def test_list_tasks_with_pagination(
        self, authenticated_client, mock_task_service
    ):
        mock_task_service.get_tasks.return_value = ([], 0)

        response = await authenticated_client.get("/api/tasks?skip=10&limit=5")

        assert response.status_code == 200
        data = response.json()
        assert data["skip"] == 10
        assert data["limit"] == 5

    async def test_list_tasks_without_token(self, unauthenticated_client):
        response = await unauthenticated_client.get("/api/tasks")

        assert response.status_code == 401
