import pytest

from src.modules.projects.schemas.project import ProjectCreate, ProjectUpdate
from src.modules.projects.schemas.project_member import ProjectMemberCreate
from src.modules.projects.use_cases.add_project_member import AddProjectMemberUseCase
from src.modules.projects.use_cases.create_project import CreateProjectUseCase
from src.modules.projects.use_cases.delete_project import DeleteProjectUseCase
from src.modules.projects.use_cases.get_project import GetProjectUseCase
from src.modules.projects.use_cases.get_project_members import GetProjectMembersUseCase
from src.modules.projects.use_cases.get_projects import GetProjectsUseCase
from src.modules.projects.use_cases.update_project import UpdateProjectUseCase
from src.modules.users.entities.user import UserRole
from src.shared.exceptions.domain import (
    AlreadyExistsError,
    ForbiddenError,
    NotFoundError,
)
from tests.conftest import make_project, make_project_member, make_user


# ---------------------------------------------------------------------------
# CreateProjectUseCase
# ---------------------------------------------------------------------------
class TestCreateProjectUseCase:
    def _make_uc(self, project_repo, user_repo, record_history):
        return CreateProjectUseCase(project_repo, user_repo, record_history)

    async def test_create_project_as_admin(
        self, project_repo, user_repo, record_history
    ):
        user_repo.get_by_id.return_value = make_user(id=1)
        project_repo.create.return_value = make_project(id=1, owner_id=1)

        uc = self._make_uc(project_repo, user_repo, record_history)
        result = await uc.execute(
            ProjectCreate(name="New Project", owner_id=1),
            actor_id=1,
            actor_role=UserRole.ADMINISTRADOR,
        )

        assert result.id == 1
        assert result.name == "Test Project"
        record_history.execute.assert_awaited_once()

    async def test_create_project_as_leader_own_project(
        self, project_repo, user_repo, record_history
    ):
        user_repo.get_by_id.return_value = make_user(id=5)
        project_repo.create.return_value = make_project(id=2, owner_id=5)

        uc = self._make_uc(project_repo, user_repo, record_history)
        result = await uc.execute(
            ProjectCreate(name="Leader Project", owner_id=5),
            actor_id=5,
            actor_role=UserRole.LIDER_PROYECTO,
        )
        assert result.id == 2

    async def test_create_project_as_leader_other_owner_forbidden(
        self, project_repo, user_repo, record_history
    ):
        user_repo.get_by_id.return_value = make_user(id=10)
        uc = self._make_uc(project_repo, user_repo, record_history)

        with pytest.raises(ForbiddenError):
            await uc.execute(
                ProjectCreate(name="Other Project", owner_id=10),
                actor_id=5,
                actor_role=UserRole.LIDER_PROYECTO,
            )

    async def test_create_project_as_user_forbidden(
        self, project_repo, user_repo, record_history
    ):
        user_repo.get_by_id.return_value = make_user(id=1)
        uc = self._make_uc(project_repo, user_repo, record_history)

        with pytest.raises(ForbiddenError):
            await uc.execute(
                ProjectCreate(name="P", owner_id=1),
                actor_id=1,
                actor_role=UserRole.USUARIO,
            )

    async def test_create_project_owner_not_found(
        self, project_repo, user_repo, record_history
    ):
        user_repo.get_by_id.return_value = None
        uc = self._make_uc(project_repo, user_repo, record_history)

        with pytest.raises(NotFoundError, match="Propietario"):
            await uc.execute(
                ProjectCreate(name="P", owner_id=999),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )


# ---------------------------------------------------------------------------
# GetProjectUseCase
# ---------------------------------------------------------------------------
class TestGetProjectUseCase:
    async def test_get_existing_project(self, project_repo):
        project_repo.get_by_id.return_value = make_project(id=1)
        uc = GetProjectUseCase(project_repo)
        result = await uc.execute(1)
        assert result.id == 1

    async def test_get_nonexistent_project(self, project_repo):
        project_repo.get_by_id.return_value = None
        uc = GetProjectUseCase(project_repo)

        with pytest.raises(NotFoundError):
            await uc.execute(999)


# ---------------------------------------------------------------------------
# GetProjectsUseCase
# ---------------------------------------------------------------------------
class TestGetProjectsUseCase:
    async def test_list_projects(self, project_repo):
        project_repo.get_all.return_value = [make_project(id=1), make_project(id=2)]
        project_repo.count.return_value = 2
        uc = GetProjectsUseCase(project_repo)

        projects, total = await uc.execute()
        assert len(projects) == 2
        assert total == 2


# ---------------------------------------------------------------------------
# UpdateProjectUseCase
# ---------------------------------------------------------------------------
class TestUpdateProjectUseCase:
    def _make_uc(self, project_repo, user_repo, record_history):
        return UpdateProjectUseCase(project_repo, user_repo, record_history)

    async def test_update_project_as_admin(
        self, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=2)
        updated = make_project(id=1, name="Updated", owner_id=2)
        project_repo.update.return_value = updated

        uc = self._make_uc(project_repo, user_repo, record_history)
        result = await uc.execute(
            1,
            ProjectUpdate(name="Updated"),
            actor_id=1,
            actor_role=UserRole.ADMINISTRADOR,
        )
        assert result.name == "Updated"

    async def test_update_project_not_found(
        self, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = None
        uc = self._make_uc(project_repo, user_repo, record_history)

        with pytest.raises(NotFoundError):
            await uc.execute(
                999,
                ProjectUpdate(name="X"),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )

    async def test_update_project_user_forbidden(
        self, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=2)
        uc = self._make_uc(project_repo, user_repo, record_history)

        with pytest.raises(ForbiddenError):
            await uc.execute(
                1,
                ProjectUpdate(name="X"),
                actor_id=3,
                actor_role=UserRole.USUARIO,
            )

    async def test_update_project_new_owner_not_found(
        self, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        user_repo.get_by_id.return_value = None
        uc = self._make_uc(project_repo, user_repo, record_history)

        with pytest.raises(NotFoundError, match="Propietario"):
            await uc.execute(
                1,
                ProjectUpdate(owner_id=999),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )


# ---------------------------------------------------------------------------
# DeleteProjectUseCase
# ---------------------------------------------------------------------------
class TestDeleteProjectUseCase:
    def _make_uc(self, project_repo, record_history):
        return DeleteProjectUseCase(project_repo, record_history)

    async def test_delete_project_as_admin(self, project_repo, record_history):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=2)
        uc = self._make_uc(project_repo, record_history)

        await uc.execute(1, actor_id=1, actor_role=UserRole.ADMINISTRADOR)
        project_repo.delete.assert_awaited_once_with(1)

    async def test_delete_project_as_owner_leader(self, project_repo, record_history):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=5)
        uc = self._make_uc(project_repo, record_history)

        await uc.execute(1, actor_id=5, actor_role=UserRole.LIDER_PROYECTO)
        project_repo.delete.assert_awaited_once()

    async def test_delete_project_forbidden(self, project_repo, record_history):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=2)
        uc = self._make_uc(project_repo, record_history)

        with pytest.raises(ForbiddenError):
            await uc.execute(1, actor_id=3, actor_role=UserRole.USUARIO)

    async def test_delete_project_not_found(self, project_repo, record_history):
        project_repo.get_by_id.return_value = None
        uc = self._make_uc(project_repo, record_history)

        with pytest.raises(NotFoundError):
            await uc.execute(999, actor_id=1, actor_role=UserRole.ADMINISTRADOR)


# ---------------------------------------------------------------------------
# GetProjectMembersUseCase
# ---------------------------------------------------------------------------
class TestGetProjectMembersUseCase:
    async def test_get_members(self, project_member_repo, project_repo):
        project_repo.get_by_id.return_value = make_project(id=1)
        project_member_repo.get_by_project.return_value = [
            make_project_member(id=1, project_id=1, user_id=2),
        ]
        project_member_repo.count_by_project.return_value = 1

        uc = GetProjectMembersUseCase(project_member_repo, project_repo)
        members, total = await uc.execute(1)
        assert len(members) == 1
        assert total == 1

    async def test_get_members_project_not_found(
        self, project_member_repo, project_repo
    ):
        project_repo.get_by_id.return_value = None
        uc = GetProjectMembersUseCase(project_member_repo, project_repo)

        with pytest.raises(NotFoundError, match="Proyecto"):
            await uc.execute(999)


# ---------------------------------------------------------------------------
# AddProjectMemberUseCase
# ---------------------------------------------------------------------------
class TestAddProjectMemberUseCase:
    def _make_uc(self, project_member_repo, project_repo, user_repo, record_history):
        return AddProjectMemberUseCase(
            project_member_repo, project_repo, user_repo, record_history
        )

    async def test_add_member_success(
        self, project_member_repo, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        user_repo.get_by_id.return_value = make_user(id=2)
        project_member_repo.get_by_project_and_user.return_value = None
        project_member_repo.create.return_value = make_project_member(
            id=1, project_id=1, user_id=2
        )

        uc = self._make_uc(project_member_repo, project_repo, user_repo, record_history)
        result = await uc.execute(
            1,
            ProjectMemberCreate(user_id=2),
            actor_id=1,
            actor_role=UserRole.ADMINISTRADOR,
        )
        assert result.user_id == 2

    async def test_add_member_already_exists(
        self, project_member_repo, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        user_repo.get_by_id.return_value = make_user(id=2)
        project_member_repo.get_by_project_and_user.return_value = make_project_member()

        uc = self._make_uc(project_member_repo, project_repo, user_repo, record_history)
        with pytest.raises(AlreadyExistsError, match="ya es miembro"):
            await uc.execute(
                1,
                ProjectMemberCreate(user_id=2),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )

    async def test_add_member_project_not_found(
        self, project_member_repo, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = None
        uc = self._make_uc(project_member_repo, project_repo, user_repo, record_history)

        with pytest.raises(NotFoundError, match="Proyecto"):
            await uc.execute(
                999,
                ProjectMemberCreate(user_id=2),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )

    async def test_add_member_user_not_found(
        self, project_member_repo, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=1)
        user_repo.get_by_id.return_value = None
        uc = self._make_uc(project_member_repo, project_repo, user_repo, record_history)

        with pytest.raises(NotFoundError, match="Usuario"):
            await uc.execute(
                1,
                ProjectMemberCreate(user_id=999),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )

    async def test_add_member_forbidden(
        self, project_member_repo, project_repo, user_repo, record_history
    ):
        project_repo.get_by_id.return_value = make_project(id=1, owner_id=2)
        user_repo.get_by_id.return_value = make_user(id=3)
        uc = self._make_uc(project_member_repo, project_repo, user_repo, record_history)

        with pytest.raises(ForbiddenError):
            await uc.execute(
                1,
                ProjectMemberCreate(user_id=3),
                actor_id=5,
                actor_role=UserRole.USUARIO,
            )
