import os
from typing import Any

from constants.default_settings_constants import (
    CLEANUP_FOLDER_PATH,
    CLEANUP_LOG_NAME,
    DEFAULT_CLEANUP_LOG_NAME,
    DEFAULT_EXCLUSION_DELAY,
    DEFAULT_EXCLUSION_FOLDER_NAME,
    DEFAULT_MOVE_DELAY,
    EXCLUSION_DELAY,
    EXCLUSION_FOLDER_NAME,
    MOVE_DELAY,
    ORGANIZATION_RULES,
    SHOULD_MOVE_FOLDER,
    UNMATCHED_FILE_ACTION,
)
from enums.unmatched_file_action_enum import UnmatchedFileActionEnum


class CleanupJob:
    """Represents a cleanup job with configuration for organizing and managing files in a specified folder.

    Attributes:
        cleanup_folder_path (str): The path to the folder where the cleanup job will be performed.
        move_delay (int): The delay (in days) before moving files. Defaults to `DEFAULT_MOVE_DELAY_DAYS` if not specified.
        exclusion_delay (int): The delay (in days) before excluding files. Defaults to `DEFAULT_EXCLUSION_DELAY_DAYS` if not specified.
        should_move_folder (bool): Indicates whether the folder should be moved. Defaults to `False`.
        exclusion_folder_name (str): The name of the folder used for exclusions. Defaults to `DEFAULT_EXCLUSION_FOLDER_NAME` if not specified.
        cleanup_log_name (str): The name of the cleanup log file. Defaults to `DEFAULT_CLEANUP_LOG_NAME` if not specified.
        unmatched_file_action (str): The action to take for unmatched files. Defaults to `UnmatchedFileActionEnum.KEEP.value` if not specified.
        organization_rules (list[dict[str, Any]]): A list of rules for organizing files. Defaults to an empty list if not specified.
        exclusion_queue_path (str): The full path to the exclusion folder within the cleanup folder.
        cleanup_log_path (str): The full path to the cleanup log file within the exclusion folder.

    Raises:
        ValueError: If `CLEANUP_FOLDER_PATH` is not specified in the job configuration.

    """

    def __init__(self, job_config: dict[str, Any]) -> None:
        if CLEANUP_FOLDER_PATH not in job_config:
            raise ValueError(f"A {CLEANUP_FOLDER_PATH} must be specified for each cleanup job.")

        self.cleanup_folder_path: str = job_config[CLEANUP_FOLDER_PATH]
        self.move_delay: int = int(job_config.get(MOVE_DELAY, DEFAULT_MOVE_DELAY))
        self.exclusion_delay: int = int(job_config.get(EXCLUSION_DELAY, DEFAULT_EXCLUSION_DELAY))
        self.should_move_folder: bool = bool(job_config.get(SHOULD_MOVE_FOLDER, False))
        self.exclusion_folder_name: str = str(job_config.get(EXCLUSION_FOLDER_NAME, DEFAULT_EXCLUSION_FOLDER_NAME))
        self.cleanup_log_name: str = str(job_config.get(CLEANUP_LOG_NAME, DEFAULT_CLEANUP_LOG_NAME))
        self.unmatched_file_action: str = str(job_config.get(UNMATCHED_FILE_ACTION, UnmatchedFileActionEnum.KEEP.value))
        self.organization_rules: list[dict[str, Any]] = list(job_config.get(ORGANIZATION_RULES, []))
        self.exclusion_queue_path: str = os.path.join(self.cleanup_folder_path, self.exclusion_folder_name)
        self.cleanup_log_path: str = os.path.join(self.exclusion_queue_path, self.cleanup_log_name)
