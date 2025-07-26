from enum import Enum


class UnmatchedFileActionEnum(Enum):
    """Enum representing actions for unmatched files."""

    KEEP = "keep"
    DELETE = "delete"
