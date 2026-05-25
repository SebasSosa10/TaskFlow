from src.modules.users.entities.user import UserRole
from src.modules.users.schemas.user import (
    UserCreate,
    UserResponse,
    UserRoleUpdate,
    UserStatusUpdate,
    UserUpdate,
)
from src.modules.users.use_cases.create_user import CreateUserUseCase
from src.modules.users.use_cases.delete_user import DeleteUserUseCase
from src.modules.users.use_cases.get_user import GetUserUseCase
from src.modules.users.use_cases.get_users import GetUsersUseCase
from src.modules.users.use_cases.update_user import UpdateUserUseCase
from src.modules.users.use_cases.update_user_role import UpdateUserRoleUseCase
from src.modules.users.use_cases.update_user_status import UpdateUserStatusUseCase


class UserService:
    def __init__(
        self,
        create_user: CreateUserUseCase,
        get_users: GetUsersUseCase,
        get_user: GetUserUseCase,
        update_user: UpdateUserUseCase,
        delete_user: DeleteUserUseCase,
        update_user_role: UpdateUserRoleUseCase,
        update_user_status: UpdateUserStatusUseCase,
    ) -> None:
        self._create_user = create_user
        self._get_users = get_users
        self._get_user = get_user
        self._update_user = update_user
        self._delete_user = delete_user
        self._update_user_role = update_user_role
        self._update_user_status = update_user_status

    async def create_user(
        self, data: UserCreate, actor_id: int, actor_role: UserRole
    ) -> UserResponse:
        return await self._create_user.execute(data, actor_id, actor_role)

    async def get_users(self, skip: int = 0, limit: int = 100) -> tuple[list[UserResponse], int]:
        return await self._get_users.execute(skip=skip, limit=limit)

    async def get_user(self, user_id: int) -> UserResponse:
        return await self._get_user.execute(user_id)

    async def update_user(
        self, user_id: int, data: UserUpdate, actor_id: int, actor_role: UserRole
    ) -> UserResponse:
        return await self._update_user.execute(user_id, data, actor_id, actor_role)

    async def delete_user(self, user_id: int, actor_id: int, actor_role: UserRole) -> None:
        await self._delete_user.execute(user_id, actor_id, actor_role)

    async def update_user_role(
        self, user_id: int, data: UserRoleUpdate, actor_id: int, actor_role: UserRole
    ) -> UserResponse:
        return await self._update_user_role.execute(user_id, data, actor_id, actor_role)

    async def update_user_status(
        self, user_id: int, data: UserStatusUpdate, actor_id: int, actor_role: UserRole
    ) -> UserResponse:
        return await self._update_user_status.execute(user_id, data, actor_id, actor_role)
