from pydantic import BaseModel, EmailStr, Field

from src.modules.users.entities.user import UserRole
from src.shared.base.schemas import BaseSchema


class LoginRequest(BaseSchema):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class RegisterRequest(BaseSchema):
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=128)
    full_name: str = Field(min_length=2, max_length=255)
    role: UserRole = UserRole.USUARIO


class TokenResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    user_id: int
    role: UserRole
