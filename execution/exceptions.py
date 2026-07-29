"""
Execution Engine exceptions.

Contains custom exceptions raised during
execution workflow.
"""


class ExecutionError(Exception):
    """
    Base exception for Execution Engine.
    """

    pass


class CommandExecutionError(ExecutionError):
    """
    Raised when command execution fails.
    """

    pass


class EnvironmentError(ExecutionError):
    """
    Raised when environment preparation fails.
    """

    pass


class SandboxError(ExecutionError):
    """
    Raised when sandbox operations fail.
    """

    pass


class ProcessError(ExecutionError):
    """
    Raised when process management fails.
    """

    pass