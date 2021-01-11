class BaseError(Exception):
    """Base class for custom exceptions"""
    pass

class CommandError(BaseError):
    """Base class for command exceptions"""
    pass

class InvalidArgumentError(CommandError):
    """Raised when an argument is invalid"""
    pass


class TooManyArgumentsError(CommandError):
    """Raised when too many arguments passed"""
    pass

class NotEnoughArgumentsError(CommandError):
    """Raised when not enough arguments passed"""
    pass

class InvalidCommandArgError(CommandError):
    """Raised when appending invalid argument to a command."""
    pass

class NoCommandError(CommandError):
    """Raised when appending invalid argument to a command."""
    pass

class MultipleExceptionsError(BaseError):
    """Raised to raise multiple exceptions at onece."""
    pass
