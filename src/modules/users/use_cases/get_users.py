from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.schemas.user import UserResponse
from src.shared.utils.mappers import user_to_response


class GetUsersUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> tuple[list[UserResponse], int]:
        users = await self.user_repository.get_all(skip=skip, limit=limit)
        total = await self.user_repository.count()
        return [user_to_response(u) for u in users], total
