from enum import Enum


class Source(Enum):
    """
    Enumeration of logging sources used for categorizing log messages.

    Each member represents a distinct component or subsystem within the application,
    enabling structured and consistent logging across modules.
    """
    logger = 'LOGGER'

    def __str__(self):
        return self.value