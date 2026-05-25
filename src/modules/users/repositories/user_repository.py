from sqlalchemy import select

from src.modules.users.entities.user import UserModel
from src.shared.base.repository import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    model = UserModel

    async def get_by_email(self, email: str) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        return result.scalar_one_or_none()
