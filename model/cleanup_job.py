"""Module for the CleanupJob class, representing a single cleanup task configuration."""

import os
from constant.folder_constants import (
    DEFAULT_CLEANUP_LOG_NAME,
    DEFAULT_EXCLUSION_FOLDER_NAME,
)
from constant.schedule_constants import DEFAULT_EXCLUSION_DELAY, DEFAULT_MOVE_DELAY


class CleanupJob:
    """Holds all configuration for a single folder cleanup task."""

    def __init__(self, job_config: dict):
        """
        Initializes a CleanupJob with settings from a dictionary object.

        Args:
            job_config (dict): A dictionary containing the configuration for one cleanup job.
        """
        if "cleanup_folder_path" not in job_config:
            raise ValueError(
                "A 'cleanup_folder_path' must be specified for each cleanup job."
            )

        self.cleanup_folder_path: str = job_config["cleanup_folder_path"]
        self.move_delay: int = int(job_config.get("move_delay", DEFAULT_MOVE_DELAY))
        self.exclusion_delay: int = int(
            job_config.get("exclusion_delay", DEFAULT_EXCLUSION_DELAY)
        )
        self.should_move_folder: bool = bool(
            job_config.get("should_move_folder", False)
        )
        self.exclusion_folder_name: str = str(
            job_config.get("exclusion_folder_name", DEFAULT_EXCLUSION_FOLDER_NAME)
        )
        self.cleanup_log_name: str = str(
            job_config.get("cleanup_log_name", DEFAULT_CLEANUP_LOG_NAME)
        )
        self.unmatched_file_action: str = str(
            job_config.get("unmatched_file_action", "delete")
        )
        self.organization_rules: list[dict] = list(
            job_config.get("organization_rules", [])
        )
        self.exclusion_queue_path: str = os.path.join(
            self.cleanup_folder_path, self.exclusion_folder_name
        )
        self.cleanup_log_path: str = os.path.join(
            self.exclusion_queue_path, self.cleanup_log_name
        )
