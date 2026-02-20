class AppException(Exception):
    """Base class for all custom application exceptions."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)