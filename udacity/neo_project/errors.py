"""Define custom errors to be used in project."""


class InvalidInputDataError(Exception):
    """Provided input data has invalid type or format."""

    def __init__(self, msg, exc=None):
        """Error constructor."""
        if exc:
            msg += f" and raised exception: {exc.__class__}: {exc}"
        super().__init__(msg)
        self.exc = exc
