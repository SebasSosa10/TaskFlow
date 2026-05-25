from datetime import timedelta

import pytest

from src.shared.security.jwt import create_access_token, decode_access_token


class TestCreateAccessToken:
    def test_creates_token_with_default_expiry(self):
        token = create_access_token({"sub": "user@test.com", "user_id": 1})
        assert isinstance(token, str)
        assert len(token) > 0

    def test_creates_token_with_custom_expiry(self):
        token = create_access_token(
            {"sub": "user@test.com"}, expires_delta=timedelta(hours=2)
        )
        assert isinstance(token, str)

    def test_token_contains_payload_data(self):
        token = create_access_token(
            {"sub": "user@test.com", "user_id": 42, "role": "admin"}
        )
        payload = decode_access_token(token)
        assert payload["sub"] == "user@test.com"
        assert payload["user_id"] == 42
        assert payload["role"] == "admin"
        assert "exp" in payload


class TestDecodeAccessToken:
    def test_decodes_valid_token(self):
        token = create_access_token({"sub": "user@test.com", "user_id": 1})
        payload = decode_access_token(token)
        assert payload["sub"] == "user@test.com"
        assert payload["user_id"] == 1

    def test_raises_on_invalid_token(self):
        with pytest.raises(ValueError, match="Token inválido o expirado"):
            decode_access_token("invalid.token.here")

    def test_raises_on_expired_token(self):
        token = create_access_token(
            {"sub": "user@test.com"}, expires_delta=timedelta(seconds=-1)
        )
        with pytest.raises(ValueError, match="Token inválido o expirado"):
            decode_access_token(token)

    def test_raises_on_tampered_token(self):
        token = create_access_token({"sub": "user@test.com"})
        tampered = token[:-5] + "XXXXX"
        with pytest.raises(ValueError, match="Token inválido o expirado"):
            decode_access_token(tampered)
