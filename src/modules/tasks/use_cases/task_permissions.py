from src.modules.tasks.entities.task import TaskModel, TaskStatus
from src.modules.users.entities.user import UserRole
from src.shared.exceptions.domain import BusinessRuleError, ForbiddenError

ALLOWED_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.PENDIENTE: {TaskStatus.EN_PROGRESO, TaskStatus.BLOQUEADA},
    TaskStatus.EN_PROGRESO: {
        TaskStatus.COMPLETADA,
        TaskStatus.BLOQUEADA,
        TaskStatus.PENDIENTE,
    },
    TaskStatus.BLOQUEADA: {TaskStatus.PENDIENTE, TaskStatus.EN_PROGRESO},
    TaskStatus.COMPLETADA: set(),
}


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    if current == new:
        return
    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if new not in allowed:
        raise BusinessRuleError(
            f"Transición de estado inválida: '{current.value}' -> '{new.value}'"
        )


def ensure_can_manage_project(role: UserRole, actor_id: int, owner_id: int) -> None:
    if role == UserRole.ADMINISTRADOR:
        return
    if role == UserRole.LIDER_PROYECTO and actor_id == owner_id:
        return
    raise ForbiddenError("No tienes permisos para gestionar tareas de este proyecto")


def ensure_can_work_on_task(
    role: UserRole, actor_id: int, owner_id: int, task: TaskModel
) -> None:
    if role == UserRole.ADMINISTRADOR:
        return
    if role == UserRole.LIDER_PROYECTO and actor_id == owner_id:
        return
    if task.assignee_id == actor_id or task.created_by_id == actor_id:
        return
    raise ForbiddenError("No tienes permisos para modificar esta tarea")
