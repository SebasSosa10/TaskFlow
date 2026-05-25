import pytest

from src.modules.tasks.entities.task import TaskStatus
from src.modules.tasks.schemas.task import (
    TaskAssignUpdate,
    TaskCreate,
    TaskStatusUpdate,
    TaskUpdate,
)
from src.modules.tasks.use_cases.assign_task import AssignTaskUseCase
from src.modules.tasks.use_cases.create_task import CreateTaskUseCase
from src.modules.tasks.use_cases.delete_task import DeleteTaskUseCase
from src.modules.tasks.use_cases.get_task import GetTaskUseCase
from src.modules.tasks.use_cases.get_tasks import GetTasksUseCase
from src.modules.tasks.use_cases.get_tasks_by_project import GetTasksByProjectUseCase
from src.modules.tasks.use_cases.get_tasks_by_status import GetTasksByStatusUseCase
from src.modules.tasks.use_cases.get_tasks_by_user import GetTasksByUserUseCase
from src.modules.tasks.use_cases.update_task import UpdateTaskUseCase
from src.modules.tasks.use_cases.update_task_status import UpdateTaskStatusUseCase
from src.modules.users.entities.user import UserRole
from src.shared.exceptions.domain import ForbiddenError, NotFoundError
from tests.conftest import make_project, make_task, make_user


# ---------------------------------------------------------------------------
# CreateTaskUseCase
# ---------------------------------------------------------------------------
class TestCreateTaskUseCase:
    def _make_uc(self, task_repo, project_repo, user_repo, record_history):
        return CreateTaskUseCase(task_repo, project_repo, user_repo, record_history)

    async def test_create_task_success(
        self, task_repo, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        task_repo.create.return_value = make_task(id=1, project_id=1, created_by_id=1)

        uc = self._make_uc(task_repo, project_repo, user_repo, record_history)
        result = await uc.execute(
            TaskCreate(title="New Task", project_id=1),
            actor_id=1,
            actor_role=UserRole.ADMINISTRADOR,
        )
        assert result.id == 1
        record_history.execute.assert_awaited_once()

    async def test_create_task_with_assignee(
        self, task_repo, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        user_repo.get_by_id.return_value = make_user(id=5)
        task_repo.create.return_value = make_task(id=1, assignee_id=5)

        uc = self._make_uc(task_repo, project_repo, user_repo, record_history)
        result = await uc.execute(
            TaskCreate(title="Task", project_id=1, assignee_id=5),
            actor_id=1,
            actor_role=UserRole.ADMINISTRADOR,
        )
        assert result.assignee_id == 5

    async def test_create_task_project_not_found(
        self, task_repo, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = None
        uc = self._make_uc(task_repo, project_repo, user_repo, record_history)

        with pytest.raises(NotFoundError, match="Proyecto"):
            await uc.execute(
                TaskCreate(title="T", project_id=999),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )

    async def test_create_task_assignee_not_found(
        self, task_repo, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        user_repo.get_by_id.return_value = None
        uc = self._make_uc(task_repo, project_repo, user_repo, record_history)

        with pytest.raises(NotFoundError, match="Usuario"):
            await uc.execute(
                TaskCreate(title="T", project_id=1, assignee_id=999),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )

    async def test_create_task_user_forbidden(
        self, task_repo, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=2)
        uc = self._make_uc(task_repo, project_repo, user_repo, record_history)

        with pytest.raises(ForbiddenError):
            await uc.execute(
                TaskCreate(title="T", project_id=1),
                actor_id=5,
                actor_role=UserRole.USUARIO,
            )


# ---------------------------------------------------------------------------
# GetTaskUseCase
# ---------------------------------------------------------------------------
class TestGetTaskUseCase:
    async def test_get_existing_task(self, task_repo):
        task_repo.get_by_id.return_value = make_task(id=1)
        uc = GetTaskUseCase(task_repo)
        result = await uc.execute(1)
        assert result.id == 1

    async def test_get_nonexistent_task(self, task_repo):
        task_repo.get_by_id.return_value = None
        uc = GetTaskUseCase(task_repo)

        with pytest.raises(NotFoundError):
            await uc.execute(999)


# ---------------------------------------------------------------------------
# GetTasksUseCase
# ---------------------------------------------------------------------------
class TestGetTasksUseCase:
    async def test_list_tasks(self, task_repo):
        task_repo.get_all.return_value = [make_task(id=1), make_task(id=2)]
        task_repo.count.return_value = 2
        uc = GetTasksUseCase(task_repo)

        tasks, total = await uc.execute()
        assert len(tasks) == 2
        assert total == 2


# ---------------------------------------------------------------------------
# GetTasksByProjectUseCase
# ---------------------------------------------------------------------------
class TestGetTasksByProjectUseCase:
    async def test_get_tasks_by_project(self, task_repo, project_repo):
        project_repo.get_by_id.return_value = make_project(id=1)
        task_repo.get_by_project.return_value = [make_task(id=1, project_id=1)]
        task_repo.count_by_project.return_value = 1

        uc = GetTasksByProjectUseCase(task_repo, project_repo)
        tasks, total = await uc.execute(1)
        assert len(tasks) == 1
        assert total == 1

    async def test_project_not_found(self, task_repo, project_repo):
        project_repo.get_by_id.return_value = None
        uc = GetTasksByProjectUseCase(task_repo, project_repo)

        with pytest.raises(NotFoundError, match="Proyecto"):
            await uc.execute(999)


# ---------------------------------------------------------------------------
# GetTasksByUserUseCase
# ---------------------------------------------------------------------------
class TestGetTasksByUserUseCase:
    async def test_get_tasks_by_user(self, task_repo, user_repo):
        user_repo.get_by_id.return_value = make_user(id=1)
        task_repo.get_by_assignee.return_value = [make_task(id=1, assignee_id=1)]
        task_repo.count_by_assignee.return_value = 1

        uc = GetTasksByUserUseCase(task_repo, user_repo)
        tasks, total = await uc.execute(1)
        assert len(tasks) == 1

    async def test_user_not_found(self, task_repo, user_repo):
        user_repo.get_by_id.return_value = None
        uc = GetTasksByUserUseCase(task_repo, user_repo)

        with pytest.raises(NotFoundError, match="Usuario"):
            await uc.execute(999)


# ---------------------------------------------------------------------------
# GetTasksByStatusUseCase
# ---------------------------------------------------------------------------
class TestGetTasksByStatusUseCase:
    async def test_get_tasks_by_status(self, task_repo):
        task_repo.get_by_status.return_value = [
            make_task(id=1, status=TaskStatus.PENDIENTE)
        ]
        task_repo.count_by_status.return_value = 1
        uc = GetTasksByStatusUseCase(task_repo)

        tasks, total = await uc.execute(TaskStatus.PENDIENTE)
        assert len(tasks) == 1
        assert total == 1


# ---------------------------------------------------------------------------
# UpdateTaskUseCase
# ---------------------------------------------------------------------------
class TestUpdateTaskUseCase:
    def _make_uc(self, task_repo, project_repo, user_repo, record_history):
        return UpdateTaskUseCase(task_repo, project_repo, user_repo, record_history)

    async def test_update_task_success(
        self, task_repo, project_repo, user_repo, record_history
    ):
        task_repo.get_by_id.return_value = make_task(id=1, project_id=1)
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        updated = make_task(id=1, title="Updated Title")
        task_repo.update.return_value = updated

        uc = self._make_uc(task_repo, project_repo, user_repo, record_history)
        result = await uc.execute(
            1,
            TaskUpdate(title="Updated Title"),
            actor_id=1,
            actor_role=UserRole.ADMINISTRADOR,
        )
        assert result.title == "Updated Title"

    async def test_update_task_not_found(
        self, task_repo, project_repo, user_repo, record_history
    ):
        task_repo.get_by_id.return_value = None
        uc = self._make_uc(task_repo, project_repo, user_repo, record_history)

        with pytest.raises(NotFoundError):
            await uc.execute(
                999,
                TaskUpdate(title="X"),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )

    async def test_update_task_forbidden(
        self, task_repo, project_repo, user_repo, record_history
    ):
        task_repo.get_by_id.return_value = make_task(id=1, project_id=1)
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=2)
        uc = self._make_uc(task_repo, project_repo, user_repo, record_history)

        with pytest.raises(ForbiddenError):
            await uc.execute(
                1,
                TaskUpdate(title="X"),
                actor_id=99,
                actor_role=UserRole.USUARIO,
            )

    async def test_update_task_validates_status_transition(
        self, task_repo, project_repo, user_repo, record_history
    ):
        task_repo.get_by_id.return_value = make_task(
            id=1, project_id=1, status=TaskStatus.COMPLETADA
        )
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        uc = self._make_uc(task_repo, project_repo, user_repo, record_history)

        from src.shared.exceptions.domain import BusinessRuleError

        with pytest.raises(BusinessRuleError):
            await uc.execute(
                1,
                TaskUpdate(status=TaskStatus.PENDIENTE),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )


# ---------------------------------------------------------------------------
# DeleteTaskUseCase
# ---------------------------------------------------------------------------
class TestDeleteTaskUseCase:
    def _make_uc(self, task_repo, project_repo, record_history):
        return DeleteTaskUseCase(task_repo, project_repo, record_history)

    async def test_delete_task_success(
        self, task_repo, project_repo, record_history
    ):
        task_repo.get_by_id.return_value = make_task(id=1, project_id=1)
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        uc = self._make_uc(task_repo, project_repo, record_history)

        await uc.execute(1, actor_id=1, actor_role=UserRole.ADMINISTRADOR)
        task_repo.delete.assert_awaited_once_with(1)

    async def test_delete_task_not_found(
        self, task_repo, project_repo, record_history
    ):
        task_repo.get_by_id.return_value = None
        uc = self._make_uc(task_repo, project_repo, record_history)

        with pytest.raises(NotFoundError):
            await uc.execute(999, actor_id=1, actor_role=UserRole.ADMINISTRADOR)

    async def test_delete_task_forbidden(
        self, task_repo, project_repo, record_history
    ):
        task_repo.get_by_id.return_value = make_task(id=1, project_id=1)
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=2)
        uc = self._make_uc(task_repo, project_repo, record_history)

        with pytest.raises(ForbiddenError):
            await uc.execute(1, actor_id=99, actor_role=UserRole.USUARIO)


# ---------------------------------------------------------------------------
# UpdateTaskStatusUseCase
# ---------------------------------------------------------------------------
class TestUpdateTaskStatusUseCase:
    def _make_uc(self, task_repo, project_repo, record_history):
        return UpdateTaskStatusUseCase(task_repo, project_repo, record_history)

    async def test_update_status_success(
        self, task_repo, project_repo, record_history
    ):
        task = make_task(
            id=1, project_id=1, status=TaskStatus.PENDIENTE,
            assignee_id=3, created_by_id=3,
        )
        task_repo.get_by_id.return_value = task
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        updated = make_task(id=1, status=TaskStatus.EN_PROGRESO)
        task_repo.update.return_value = updated

        uc = self._make_uc(task_repo, project_repo, record_history)
        result = await uc.execute(
            1,
            TaskStatusUpdate(status=TaskStatus.EN_PROGRESO),
            actor_id=3,
            actor_role=UserRole.USUARIO,
        )
        assert result.status == TaskStatus.EN_PROGRESO

    async def test_update_status_invalid_transition(
        self, task_repo, project_repo, record_history
    ):
        task = make_task(
            id=1, project_id=1, status=TaskStatus.COMPLETADA,
            assignee_id=1, created_by_id=1,
        )
        task_repo.get_by_id.return_value = task
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        uc = self._make_uc(task_repo, project_repo, record_history)

        from src.shared.exceptions.domain import BusinessRuleError

        with pytest.raises(BusinessRuleError):
            await uc.execute(
                1,
                TaskStatusUpdate(status=TaskStatus.PENDIENTE),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )

    async def test_update_status_task_not_found(
        self, task_repo, project_repo, record_history
    ):
        task_repo.get_by_id.return_value = None
        uc = self._make_uc(task_repo, project_repo, record_history)

        with pytest.raises(NotFoundError):
            await uc.execute(
                999,
                TaskStatusUpdate(status=TaskStatus.EN_PROGRESO),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )


# ---------------------------------------------------------------------------
# AssignTaskUseCase
# ---------------------------------------------------------------------------
class TestAssignTaskUseCase:
    def _make_uc(self, task_repo, project_repo, user_repo, record_history):
        return AssignTaskUseCase(task_repo, project_repo, user_repo, record_history)

    async def test_assign_task_success(
        self, task_repo, project_repo, user_repo, record_history
    ):
        task_repo.get_by_id.return_value = make_task(id=1, project_id=1)
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        user_repo.get_by_id.return_value = make_user(id=5)
        updated = make_task(id=1, assignee_id=5)
        task_repo.update.return_value = updated

        uc = self._make_uc(task_repo, project_repo, user_repo, record_history)
        result = await uc.execute(
            1,
            TaskAssignUpdate(assignee_id=5),
            actor_id=1,
            actor_role=UserRole.ADMINISTRADOR,
        )
        assert result.assignee_id == 5

    async def test_assign_task_not_found(
        self, task_repo, project_repo, user_repo, record_history
    ):
        task_repo.get_by_id.return_value = None
        uc = self._make_uc(task_repo, project_repo, user_repo, record_history)

        with pytest.raises(NotFoundError):
            await uc.execute(
                999,
                TaskAssignUpdate(assignee_id=5),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )

    async def test_assign_task_assignee_not_found(
        self, task_repo, project_repo, user_repo, record_history
    ):
        task_repo.get_by_id.return_value = make_task(id=1, project_id=1)
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        user_repo.get_by_id.return_value = None
        uc = self._make_uc(task_repo, project_repo, user_repo, record_history)

        with pytest.raises(NotFoundError, match="Usuario"):
            await uc.execute(
                1,
                TaskAssignUpdate(assignee_id=999),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )

    async def test_assign_task_forbidden(
        self, task_repo, project_repo, user_repo, record_history
    ):
        task_repo.get_by_id.return_value = make_task(id=1, project_id=1)
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=2)
        uc = self._make_uc(task_repo, project_repo, user_repo, record_history)

        with pytest.raises(ForbiddenError):
            await uc.execute(
                1,
                TaskAssignUpdate(assignee_id=5),
                actor_id=99,
                actor_role=UserRole.USUARIO,
            )
