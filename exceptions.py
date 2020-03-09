class BaseError(Exception):
    """Base class for custom exceptions"""
    pass

class InvalidArgument(BaseError):
    """Raised when an argument is invalid"""
    pass


class TooManyArguments(BaseError):
    """Raised when an argument is invalid"""
    pass
