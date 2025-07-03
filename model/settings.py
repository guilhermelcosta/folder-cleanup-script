"""Settings module for cleanup and exclusion folder configuration.

This module defines the Settings class, which holds configuration for cleanup and exclusion folders,
file names, and log paths.
"""

import os

from constant.folder_constants import (
    DEFAULT_CLEANUP_FOLDER_NAME,
    DEFAULT_CLEANUP_LOG_NAME,
    DEFAULT_EXCLUSION_FOLDER_NAME,
)
from constant.schedule_constants import DEFAULT_EXCLUSION_DELAY, DEFAULT_MOVE_DELAY


class Settings:
    """Holds configuration for cleanup and exclusion folders, file names, and log paths."""

    def __init__(self, object: dict[str, str]) -> None:
        """Initialize Settings with default folder and file names/paths."""
        self.move_delay = object.get("move_delay", DEFAULT_MOVE_DELAY)
        self.exclusion_delay = object.get("exclusion_delay", DEFAULT_EXCLUSION_DELAY)
        self.should_move_folder = object.get("should_move_folder", False)
        self.cleanup_folder_name = object.get("cleanup_folder_name", DEFAULT_CLEANUP_FOLDER_NAME)
        self.exclusion_folder_name = object.get("exclusion_folder_name", DEFAULT_EXCLUSION_FOLDER_NAME)
        self.cleanup_log_name = object.get("cleanup_log_name", DEFAULT_CLEANUP_LOG_NAME)
        self.cleanup_folder_path = object.get(
            "cleanup_folder_path", os.path.expanduser(f"~/{self.cleanup_folder_name}")
        )
        self.exclusion_queue_path = object.get(
            "exclusion_queue_path", os.path.join(self.cleanup_folder_path, self.exclusion_folder_name)
        )
        self.cleanup_log_path = object.get(
            "cleanup_log_path", os.path.join(self.exclusion_queue_path, self.cleanup_log_name)
        )
