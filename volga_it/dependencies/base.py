from fastapi import HTTPException, status


class BaseDependency:
    FORBIDDEN = HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    def __init__(self, *, auto_error=True) -> None:
        self.auto_error = auto_error
