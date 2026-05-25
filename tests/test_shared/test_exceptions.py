from src.shared.exceptions.domain import (
    AlreadyExistsError,
    BusinessRuleError,
    DomainException,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)


class TestDomainExceptions:
    def test_not_found_error(self):
        exc = NotFoundError("Recurso no encontrado")
        assert exc.message == "Recurso no encontrado"
        assert str(exc) == "Recurso no encontrado"
        assert isinstance(exc, DomainException)

    def test_already_exists_error(self):
        exc = AlreadyExistsError("Ya existe")
        assert exc.message == "Ya existe"
        assert isinstance(exc, DomainException)

    def test_unauthorized_error(self):
        exc = UnauthorizedError("No autorizado")
        assert exc.message == "No autorizado"
        assert isinstance(exc, DomainException)

    def test_forbidden_error(self):
        exc = ForbiddenError("Prohibido")
        assert exc.message == "Prohibido"
        assert isinstance(exc, DomainException)

    def test_validation_error(self):
        exc = ValidationError("Dato inválido")
        assert exc.message == "Dato inválido"
        assert isinstance(exc, DomainException)

    def test_business_rule_error(self):
        exc = BusinessRuleError("Regla violada")
        assert exc.message == "Regla violada"
        assert isinstance(exc, DomainException)

    def test_all_are_catchable_as_domain_exception(self):
        exceptions = [
            NotFoundError("a"),
            AlreadyExistsError("b"),
            UnauthorizedError("c"),
            ForbiddenError("d"),
            ValidationError("e"),
            BusinessRuleError("f"),
        ]
        for exc in exceptions:
            assert isinstance(exc, DomainException)
            assert isinstance(exc, Exception)
