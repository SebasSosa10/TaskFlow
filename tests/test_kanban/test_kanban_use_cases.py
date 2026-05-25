import pytest

from src.modules.kanban.use_cases.get_kanban_board import GetKanbanBoardUseCase
from src.modules.tasks.entities.task import TaskStatus
from src.shared.exceptions.domain import NotFoundError
from tests.conftest import make_project, make_task


class TestGetKanbanBoardUseCase:
    async def test_get_board_success(self, project_repo, task_repo):
        project_repo.get_by_id.return_value = make_project(id=1, name="My Project")
        task_repo.get_by_project_and_status.side_effect = lambda pid, status: {
            TaskStatus.PENDIENTE: [make_task(id=1, status=TaskStatus.PENDIENTE)],
            TaskStatus.EN_PROGRESO: [make_task(id=2, status=TaskStatus.EN_PROGRESO)],
            TaskStatus.COMPLETADA: [],
            TaskStatus.BLOQUEADA: [],
        }[status]

        uc = GetKanbanBoardUseCase(project_repo, task_repo)
        result = await uc.execute(1)

        assert result.project_id == 1
        assert result.project_name == "My Project"
        assert len(result.columns) == 4
        assert len(result.columns[0].tasks) == 1
        assert result.columns[0].status == TaskStatus.PENDIENTE

    async def test_get_board_empty_project(self, project_repo, task_repo):
        project_repo.get_by_id.return_value = make_project(id=1)
        task_repo.get_by_project_and_status.return_value = []

        uc = GetKanbanBoardUseCase(project_repo, task_repo)
        result = await uc.execute(1)

        assert all(len(col.tasks) == 0 for col in result.columns)

    async def test_get_board_project_not_found(self, project_repo, task_repo):
        project_repo.get_by_id.return_value = None
        uc = GetKanbanBoardUseCase(project_repo, task_repo)

        with pytest.raises(NotFoundError, match="Proyecto"):
            await uc.execute(999)
