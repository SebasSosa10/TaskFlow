from pydantic import EmailStr, Field

from src.modules.users.entities.user import UserRole
from src.shared.base.schemas import BaseSchema, TimestampMixin


class UserCreate(BaseSchema):
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=128)
    full_name: str = Field(min_length=2, max_length=255)
    role: UserRole = UserRole.USUARIO
    is_active: bool = True


class UserUpdate(BaseSchema):
    email: EmailStr | None = None
    username: str | None = Field(default=None, min_length=3, max_length=100)
    password: str | None = Field(default=None, min_length=6, max_length=128)
    full_name: str | None = Field(default=None, min_length=2, max_length=255)
    role: UserRole | None = None
    is_active: bool | None = None


class UserRoleUpdate(BaseSchema):
    role: UserRole


class UserStatusUpdate(BaseSchema):
    is_active: bool


class UserResponse(TimestampMixin):
    id: int
    email: EmailStr
    username: str
    full_name: str
    role: UserRole
    is_active: bool
