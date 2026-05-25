from src.modules.tasks.entities.task import TaskStatus
from src.modules.tasks.schemas.task import (
    TaskAssignUpdate,
    TaskCreate,
    TaskResponse,
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


class TaskService:
    def __init__(
        self,
        create_task: CreateTaskUseCase,
        get_tasks: GetTasksUseCase,
        get_task: GetTaskUseCase,
        get_tasks_by_project: GetTasksByProjectUseCase,
        get_tasks_by_user: GetTasksByUserUseCase,
        get_tasks_by_status: GetTasksByStatusUseCase,
        update_task: UpdateTaskUseCase,
        delete_task: DeleteTaskUseCase,
        update_status: UpdateTaskStatusUseCase,
        assign_task: AssignTaskUseCase,
    ) -> None:
        self._create_task = create_task
        self._get_tasks = get_tasks
        self._get_task = get_task
        self._get_tasks_by_project = get_tasks_by_project
        self._get_tasks_by_user = get_tasks_by_user
        self._get_tasks_by_status = get_tasks_by_status
        self._update_task = update_task
        self._delete_task = delete_task
        self._update_status = update_status
        self._assign_task = assign_task

    async def create_task(
        self, data: TaskCreate, actor_id: int, actor_role: UserRole
    ) -> TaskResponse:
        return await self._create_task.execute(data, actor_id, actor_role)

    async def get_tasks(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[list[TaskResponse], int]:
        return await self._get_tasks.execute(skip=skip, limit=limit)

    async def get_task(self, task_id: int) -> TaskResponse:
        return await self._get_task.execute(task_id)

    async def get_tasks_by_project(
        self, project_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[TaskResponse], int]:
        return await self._get_tasks_by_project.execute(
            project_id, skip=skip, limit=limit
        )

    async def get_tasks_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[TaskResponse], int]:
        return await self._get_tasks_by_user.execute(user_id, skip=skip, limit=limit)

    async def get_tasks_by_status(
        self, status: TaskStatus, skip: int = 0, limit: int = 100
    ) -> tuple[list[TaskResponse], int]:
        return await self._get_tasks_by_status.execute(status, skip=skip, limit=limit)

    async def update_task(
        self, task_id: int, data: TaskUpdate, actor_id: int, actor_role: UserRole
    ) -> TaskResponse:
        return await self._update_task.execute(task_id, data, actor_id, actor_role)

    async def delete_task(
        self, task_id: int, actor_id: int, actor_role: UserRole
    ) -> None:
        await self._delete_task.execute(task_id, actor_id, actor_role)

    async def update_status(
        self,
        task_id: int,
        data: TaskStatusUpdate,
        actor_id: int,
        actor_role: UserRole,
    ) -> TaskResponse:
        return await self._update_status.execute(task_id, data, actor_id, actor_role)

    async def assign_task(
        self,
        task_id: int,
        data: TaskAssignUpdate,
        actor_id: int,
        actor_role: UserRole,
    ) -> TaskResponse:
        return await self._assign_task.execute(task_id, data, actor_id, actor_role)
