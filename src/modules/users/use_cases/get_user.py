from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.schemas.user import UserResponse
from src.shared.exceptions.domain import NotFoundError
from src.shared.utils.mappers import user_to_response


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"Recurso con id {user_id} no encontrado")
        return user_to_response(user)
