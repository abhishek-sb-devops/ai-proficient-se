class DomainException(Exception):
    """Base exception for all domain-specific errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class URLNotFoundException(DomainException):
    """Raised when a short code does not exist in the repository."""

    pass


class AliasConflictException(DomainException):
    """Raised when a requested custom alias is already occupied."""

    pass


class InvalidURLSchemeException(DomainException):
    """Raised when the URL scheme is unsupported or invalid."""

    pass
