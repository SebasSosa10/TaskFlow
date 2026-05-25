from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from src.modules.projects.entities.project import ProjectStatus
from src.modules.tasks.entities.task import TaskStatus
from src.modules.users.entities.user import UserRole


def make_user(
    id: int = 1,
    email: str = "test@example.com",
    username: str = "testuser",
    hashed_password: str = "hashed_pw",
    full_name: str = "Test User",
    role: UserRole = UserRole.USUARIO,
    is_active: bool = True,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=id,
        email=email,
        username=username,
        hashed_password=hashed_password,
        full_name=full_name,
        role=role,
        is_active=is_active,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


def make_project(
    id: int = 1,
    name: str = "Test Project",
    description: str = "A test project",
    owner_id: int = 1,
    status: ProjectStatus = ProjectStatus.ACTIVO,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=id,
        name=name,
        description=description,
        owner_id=owner_id,
        status=status,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


def make_task(
    id: int = 1,
    title: str = "Test Task",
    description: str = "A test task",
    status: TaskStatus = TaskStatus.PENDIENTE,
    priority: int = 1,
    project_id: int = 1,
    assignee_id: int | None = None,
    created_by_id: int = 1,
    due_date: datetime | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=id,
        title=title,
        description=description,
        status=status,
        priority=priority,
        project_id=project_id,
        assignee_id=assignee_id,
        created_by_id=created_by_id,
        due_date=due_date,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


def make_history(
    id: int = 1,
    user_id: int = 1,
    action: str = "create",
    entity_type: str = "user",
    entity_id: int = 1,
    details: str = "Detalle",
) -> SimpleNamespace:
    return SimpleNamespace(
        id=id,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details,
        created_at=datetime.now(timezone.utc),
    )


def make_project_member(
    id: int = 1, project_id: int = 1, user_id: int = 2
) -> SimpleNamespace:
    return SimpleNamespace(
        id=id,
        project_id=project_id,
        user_id=user_id,
        joined_at=datetime.now(timezone.utc),
    )


def make_notification(
    id: int = 1,
    user_id: int = 1,
    title: str = "Notificación",
    message: str = "Mensaje de prueba",
    is_read: bool = False,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=id,
        user_id=user_id,
        title=title,
        message=message,
        is_read=is_read,
        created_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def user_repo():
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_email = AsyncMock()
    repo.get_by_username = AsyncMock()
    repo.get_all = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    repo.count = AsyncMock()
    return repo


@pytest.fixture
def project_repo():
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_all = AsyncMock()
    repo.get_by_owner = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    repo.count = AsyncMock()
    return repo


@pytest.fixture
def project_member_repo():
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_project = AsyncMock()
    repo.get_by_project_and_user = AsyncMock()
    repo.create = AsyncMock()
    repo.count_by_project = AsyncMock()
    return repo


@pytest.fixture
def task_repo():
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_all = AsyncMock()
    repo.get_by_project = AsyncMock()
    repo.get_by_assignee = AsyncMock()
    repo.get_by_status = AsyncMock()
    repo.get_by_project_and_status = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    repo.count = AsyncMock()
    repo.count_by_project = AsyncMock()
    repo.count_by_assignee = AsyncMock()
    repo.count_by_status = AsyncMock()
    repo.count_by_project_and_status = AsyncMock()
    return repo


@pytest.fixture
def history_repo():
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_all = AsyncMock()
    repo.get_by_user = AsyncMock()
    repo.get_by_entity = AsyncMock()
    repo.create = AsyncMock()
    repo.count = AsyncMock()
    repo.count_by_user = AsyncMock()
    return repo


@pytest.fixture
def notification_repo():
    repo = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_user = AsyncMock()
    repo.create = AsyncMock()
    repo.count_by_user = AsyncMock()
    return repo


@pytest.fixture
def record_history():
    return AsyncMock()
