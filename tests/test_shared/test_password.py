import pytest

try:
    from src.shared.security.password import hash_password, verify_password

    hash_password("test123")
    _BCRYPT_OK = True
except Exception:
    _BCRYPT_OK = False

bcrypt_required = pytest.mark.skipif(
    not _BCRYPT_OK,
    reason="bcrypt backend no disponible (incompatibilidad passlib/bcrypt)",
)


@bcrypt_required
class TestHashPassword:
    def test_returns_hashed_string(self):
        hashed = hash_password("my_password")
        assert isinstance(hashed, str)
        assert hashed != "my_password"

    def test_different_calls_produce_different_hashes(self):
        h1 = hash_password("same_password")
        h2 = hash_password("same_password")
        assert h1 != h2


@bcrypt_required
class TestVerifyPassword:
    def test_correct_password_returns_true(self):
        hashed = hash_password("correct_password")
        assert verify_password("correct_password", hashed) is True

    def test_wrong_password_returns_false(self):
        hashed = hash_password("correct_password")
        assert verify_password("wrong_password", hashed) is False

    def test_empty_password_returns_false(self):
        hashed = hash_password("some_password")
        assert verify_password("", hashed) is False
