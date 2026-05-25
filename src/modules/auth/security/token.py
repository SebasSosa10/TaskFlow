from datetime import timedelta
from typing import Any

from src.shared.security.jwt import create_access_token as _create_access_token
from src.shared.security.jwt import decode_access_token as _decode_access_token


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    return _create_access_token(data, expires_delta=expires_delta)


def decode_access_token(token: str) -> dict[str, Any]:
    return _decode_access_token(token)
