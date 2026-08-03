"""
Git Safety Layer Exceptions.

Contains all Git related exceptions used by CodePilot.
"""


class GitError(Exception):
    """
    Base exception for Git operations.
    """

    pass


class NotAGitRepositoryError(GitError):
    """
    Raised when repository is not a git repository.
    """

    pass


class GitCommandError(GitError):
    """
    Raised when a git command fails.
    """

    def __init__(
        self,
        command: str,
        message: str,
    ) -> None:

        self.command = command
        self.message = message

        super().__init__(
            f"Git command failed: {command}\n{message}"
        )


class SnapshotError(GitError):
    """
    Raised when snapshot creation or restoration fails.
    """

    pass