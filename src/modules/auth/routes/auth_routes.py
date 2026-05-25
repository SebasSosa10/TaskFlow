from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.modules.auth.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from src.modules.auth.services.auth_service import AuthService
from src.shared.base.schemas import ErrorResponse
from src.shared.exceptions.domain import (
    AlreadyExistsError,
    DomainException,
    ForbiddenError,
    UnauthorizedError,
)
from src.shared.middleware.dependencies import get_auth_service, get_current_active_user
from src.modules.users.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Credenciales inválidas"},
        403: {"model": ErrorResponse, "description": "Usuario inactivo"},
    },
    summary="Iniciar sesión",
)
async def login(
    credentials: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenResponse:
    try:
        return await auth_service.login(credentials)
    except (UnauthorizedError, ForbiddenError) as exc:
        status_code = (
            status.HTTP_401_UNAUTHORIZED
            if isinstance(exc, UnauthorizedError)
            else status.HTTP_403_FORBIDDEN
        )
        raise HTTPException(status_code=status_code, detail=exc.message) from exc


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse, "description": "Usuario ya existe"},
        403: {"model": ErrorResponse, "description": "Registro no permitido"},
    },
    summary="Registrar usuario",
)
async def register(
    data: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserResponse:
    try:
        return await auth_service.register(data)
    except (AlreadyExistsError, ForbiddenError) as exc:
        status_code = (
            status.HTTP_409_CONFLICT
            if isinstance(exc, AlreadyExistsError)
            else status.HTTP_403_FORBIDDEN
        )
        raise HTTPException(status_code=status_code, detail=exc.message) from exc
    except DomainException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message) from exc


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={401: {"model": ErrorResponse, "description": "No autenticado"}},
    summary="Obtener usuario autenticado",
)
async def get_me(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
) -> UserResponse:
    return current_user
