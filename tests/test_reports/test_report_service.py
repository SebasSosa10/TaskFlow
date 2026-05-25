from src.modules.reports.services.report_service import ReportService
from src.modules.tasks.entities.task import TaskStatus
from src.modules.users.entities.user import UserRole
from tests.conftest import make_project, make_task, make_user


class TestPerformanceReport:
    async def test_performance_report_with_data(
        self, user_repo, project_repo, task_repo
    ):
        user1 = make_user(id=1, username="alice", full_name="Alice A")
        user_repo.get_all.return_value = [user1]
        user_repo.count.return_value = 1
        task_repo.count.return_value = 3
        task_repo.count_by_status.return_value = 1

        completed_task = make_task(id=1, status=TaskStatus.COMPLETADA, assignee_id=1)
        pending_task = make_task(id=2, status=TaskStatus.PENDIENTE, assignee_id=1)
        task_repo.get_by_assignee.return_value = [completed_task, pending_task]

        service = ReportService(user_repo, project_repo, task_repo)
        report = await service.get_performance_report()

        assert report.total_users == 1
        assert report.total_tasks == 3
        assert report.completed_tasks == 1
        assert len(report.users) == 1
        assert report.users[0].assigned_tasks == 2
        assert report.users[0].completed_tasks == 1
        assert report.users[0].completion_rate == 50.0

    async def test_performance_report_no_tasks(
        self, user_repo, project_repo, task_repo
    ):
        user_repo.get_all.return_value = [make_user(id=1)]
        user_repo.count.return_value = 1
        task_repo.count.return_value = 0
        task_repo.count_by_status.return_value = 0
        task_repo.get_by_assignee.return_value = []

        service = ReportService(user_repo, project_repo, task_repo)
        report = await service.get_performance_report()

        assert report.overall_completion_rate == 0.0
        assert report.users[0].completion_rate == 0.0


class TestProjectsReport:
    async def test_projects_report(self, user_repo, project_repo, task_repo):
        project_repo.get_all.return_value = [make_project(id=1, name="Proj1")]
        project_repo.count.return_value = 1
        task_repo.count_by_project.return_value = 10
        task_repo.count_by_project_and_status.side_effect = lambda pid, status: {
            TaskStatus.COMPLETADA: 5,
            TaskStatus.EN_PROGRESO: 3,
            TaskStatus.PENDIENTE: 1,
            TaskStatus.BLOQUEADA: 1,
        }[status]

        service = ReportService(user_repo, project_repo, task_repo)
        report = await service.get_projects_report()

        assert report.total_projects == 1
        item = report.projects[0]
        assert item.total_tasks == 10
        assert item.completed_tasks == 5
        assert item.completion_rate == 50.0


class TestTasksReport:
    async def test_tasks_report(self, user_repo, project_repo, task_repo):
        task_repo.count.return_value = 20
        task_repo.count_by_status.side_effect = lambda s: {
            TaskStatus.PENDIENTE: 5,
            TaskStatus.EN_PROGRESO: 8,
            TaskStatus.COMPLETADA: 4,
            TaskStatus.BLOQUEADA: 3,
        }[s]

        service = ReportService(user_repo, project_repo, task_repo)
        report = await service.get_tasks_report()

        assert report.total_tasks == 20
        assert len(report.by_status) == 4
        status_map = {s.status: s.count for s in report.by_status}
        assert status_map[TaskStatus.PENDIENTE] == 5
        assert status_map[TaskStatus.COMPLETADA] == 4


class TestUsersReport:
    async def test_users_report(self, user_repo, project_repo, task_repo):
        user = make_user(
            id=1,
            username="alice",
            full_name="Alice",
            email="alice@test.com",
            role=UserRole.USUARIO,
        )
        user_repo.get_all.return_value = [user]
        user_repo.count.return_value = 1
        project_repo.get_by_owner.return_value = [make_project(id=1)]
        task_repo.get_by_assignee.return_value = [make_task(id=1), make_task(id=2)]

        service = ReportService(user_repo, project_repo, task_repo)
        report = await service.get_users_report()

        assert report.total_users == 1
        item = report.users[0]
        assert item.owned_projects == 1
        assert item.assigned_tasks == 2
