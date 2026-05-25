import pytest

from src.modules.tasks.entities.task import TaskStatus
from src.modules.tasks.use_cases.task_permissions import (
    ensure_can_manage_project,
    ensure_can_work_on_task,
    validate_status_transition,
)
from src.modules.users.entities.user import UserRole
from src.shared.exceptions.domain import BusinessRuleError, ForbiddenError
from tests.conftest import make_task


class TestValidateStatusTransition:
    def test_same_status_allowed(self):
        validate_status_transition(TaskStatus.PENDIENTE, TaskStatus.PENDIENTE)

    def test_pendiente_to_en_progreso(self):
        validate_status_transition(TaskStatus.PENDIENTE, TaskStatus.EN_PROGRESO)

    def test_pendiente_to_bloqueada(self):
        validate_status_transition(TaskStatus.PENDIENTE, TaskStatus.BLOQUEADA)

    def test_pendiente_to_completada_forbidden(self):
        with pytest.raises(BusinessRuleError, match="Transición de estado inválida"):
            validate_status_transition(TaskStatus.PENDIENTE, TaskStatus.COMPLETADA)

    def test_en_progreso_to_completada(self):
        validate_status_transition(TaskStatus.EN_PROGRESO, TaskStatus.COMPLETADA)

    def test_en_progreso_to_bloqueada(self):
        validate_status_transition(TaskStatus.EN_PROGRESO, TaskStatus.BLOQUEADA)

    def test_en_progreso_to_pendiente(self):
        validate_status_transition(TaskStatus.EN_PROGRESO, TaskStatus.PENDIENTE)

    def test_bloqueada_to_pendiente(self):
        validate_status_transition(TaskStatus.BLOQUEADA, TaskStatus.PENDIENTE)

    def test_bloqueada_to_en_progreso(self):
        validate_status_transition(TaskStatus.BLOQUEADA, TaskStatus.EN_PROGRESO)

    def test_bloqueada_to_completada_forbidden(self):
        with pytest.raises(BusinessRuleError):
            validate_status_transition(TaskStatus.BLOQUEADA, TaskStatus.COMPLETADA)

    def test_completada_to_any_forbidden(self):
        for target in [
            TaskStatus.PENDIENTE,
            TaskStatus.EN_PROGRESO,
            TaskStatus.BLOQUEADA,
        ]:
            with pytest.raises(BusinessRuleError):
                validate_status_transition(TaskStatus.COMPLETADA, target)


class TestEnsureCanManageProject:
    def test_admin_always_allowed(self):
        ensure_can_manage_project(UserRole.ADMINISTRADOR, actor_id=1, owner_id=99)

    def test_leader_own_project_allowed(self):
        ensure_can_manage_project(UserRole.LIDER_PROYECTO, actor_id=5, owner_id=5)

    def test_leader_other_project_forbidden(self):
        with pytest.raises(ForbiddenError):
            ensure_can_manage_project(UserRole.LIDER_PROYECTO, actor_id=5, owner_id=10)

    def test_user_forbidden(self):
        with pytest.raises(ForbiddenError):
            ensure_can_manage_project(UserRole.USUARIO, actor_id=1, owner_id=1)


class TestEnsureCanWorkOnTask:
    def test_admin_always_allowed(self):
        task = make_task(assignee_id=99, created_by_id=99)
        ensure_can_work_on_task(
            UserRole.ADMINISTRADOR, actor_id=1, owner_id=50, task=task
        )

    def test_leader_own_project_allowed(self):
        task = make_task(assignee_id=99, created_by_id=99)
        ensure_can_work_on_task(
            UserRole.LIDER_PROYECTO, actor_id=5, owner_id=5, task=task
        )

    def test_assignee_allowed(self):
        task = make_task(assignee_id=3, created_by_id=99)
        ensure_can_work_on_task(UserRole.USUARIO, actor_id=3, owner_id=50, task=task)

    def test_creator_allowed(self):
        task = make_task(assignee_id=99, created_by_id=3)
        ensure_can_work_on_task(UserRole.USUARIO, actor_id=3, owner_id=50, task=task)

    def test_unrelated_user_forbidden(self):
        task = make_task(assignee_id=10, created_by_id=20)
        with pytest.raises(ForbiddenError):
            ensure_can_work_on_task(
                UserRole.USUARIO, actor_id=99, owner_id=50, task=task
            )
