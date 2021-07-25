class InvalidInputDataError(Exception):
    "Provided input data has invalid type or format"

    def __init__(self, msg, exc=None):
        if exc:
            msg += f" and raised exception: {exc.__class__}: {exc}"
        super().__init__(msg)
        self.exc = exc
