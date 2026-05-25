class DomainException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NotFoundError(DomainException):
    pass


class AlreadyExistsError(DomainException):
    pass


class UnauthorizedError(DomainException):
    pass


class ForbiddenError(DomainException):
    pass


class ValidationError(DomainException):
    pass


class BusinessRuleError(DomainException):
    pass
