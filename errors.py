class LogFileIsADirectory(Exception):
    """Raised when provided log file is a directory."""

    def __init__(self, path):
        super().__init__(f'Provided logging file ("{path}") is a directory.')


class LogPathDoesNotExist(Exception):
    """Raised when provided log path does not exist."""

    def __init__(self, path):
        super().__init__(
            f'Provided logging directory ("{path}") does not exist '
            "or is not a directory."
        )


class LogPathInsufficientPermissions(Exception):
    """Raised when user does not have permissions read and/or write to provided log path."""

    def __init__(self, path):
        super().__init__(
            "You do not have permissions to read and/or write "
            f'to provided logging directory ("{path}").'
        )
