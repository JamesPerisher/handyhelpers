class BaseError(Exception):
    """Base class for custom exceptions"""
    pass

class CommandError(BaseError):
    """Base class for command exceptions"""
    pass

class InvalidArgument(CommandError):
    """Raised when an argument is invalid"""
    pass


class TooManyArguments(CommandError):
    """Raised when too many arguments passed"""
    pass

class NotEnoughArguments(CommandError):
    """Raised when not enough arguments passed"""
    pass

class InvalidCommandArg(CommandError):
    """Raised when appending invalid argument to a command."""
    pass


class MultipleExceptions(BaseError):
    """Raised to raise multiple exceptions at onece."""
    pass
