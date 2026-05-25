from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.modules.auth.schemas.auth import TokenResponse
from src.modules.auth.services.auth_service import AuthService
from src.modules.projects.schemas.project import ProjectResponse
from src.modules.projects.services.project_service import ProjectService
from src.modules.tasks.schemas.task import TaskResponse
from src.modules.tasks.services.task_service import TaskService
from src.modules.users.entities.user import UserRole
from src.modules.users.schemas.user import UserResponse
from src.shared.middleware.dependencies import (
    get_auth_service,
    get_current_active_user,
    get_project_service,
    get_task_service,
)

NOW = datetime.now(timezone.utc)

ADMIN_USER = UserResponse(
    id=1,
    email="admin@taskflow.com",
    username="admin",
    full_name="Admin User",
    role=UserRole.ADMINISTRADOR,
    is_active=True,
    created_at=NOW,
    updated_at=NOW,
)

REGULAR_USER = UserResponse(
    id=2,
    email="user@taskflow.com",
    username="regularuser",
    full_name="Regular User",
    role=UserRole.USUARIO,
    is_active=True,
    created_at=NOW,
    updated_at=NOW,
)

SAMPLE_TASK = TaskResponse(
    id=1,
    title="Sample Task",
    description="A sample task",
    status="pendiente",
    priority=1,
    project_id=1,
    assignee_id=2,
    created_by_id=1,
    due_date=None,
    created_at=NOW,
    updated_at=NOW,
)

SAMPLE_PROJECT = ProjectResponse(
    id=1,
    name="Sample Project",
    description="A sample project",
    owner_id=1,
    status="activo",
    created_at=NOW,
    updated_at=NOW,
)


@pytest.fixture
def mock_auth_service():
    service = AsyncMock(spec=AuthService)
    return service


@pytest.fixture
def mock_task_service():
    service = AsyncMock(spec=TaskService)
    return service


@pytest.fixture
def mock_project_service():
    service = AsyncMock(spec=ProjectService)
    return service


@pytest.fixture
async def authenticated_client(
    mock_auth_service, mock_task_service, mock_project_service
):
    app.dependency_overrides[get_current_active_user] = lambda: ADMIN_USER
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
    app.dependency_overrides[get_task_service] = lambda: mock_task_service
    app.dependency_overrides[get_project_service] = lambda: mock_project_service

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def unauthenticated_client(mock_auth_service):
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
    app.dependency_overrides.pop(get_current_active_user, None)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
