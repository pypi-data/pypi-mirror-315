from enum import StrEnum


class SessionScope(StrEnum):
    TEMPORARY = 'temporary'
    PERSISTENT = 'persistent'
