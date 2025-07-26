# attributes for default setting
from typing import Any, Final

from enums.organization_type_enum import OrganizationTypeEnum
from enums.unmatched_file_action_enum import UnmatchedFileActionEnum
from pathlib import Path

# attribute settings
CLEANUP_FOLDER_PATH: Final[str] = "cleanup_folder_path"
MOVE_DELAY: Final[str] = "move_delay"
EXCLUSION_DELAY: Final[str] = "exclusion_delay"
SHOULD_MOVE_FOLDER: Final[str] = "should_move_folder"
EXCLUSION_FOLDER_NAME: Final[str] = "exclusion_folder_name"
CLEANUP_LOG_NAME: Final[str] = "cleanup_log_name"
UNMATCHED_FILE_ACTION: Final[str] = "unmatched_file_action"
ORGANIZATION_RULES: Final[str] = "organization_rules"
PRIORITY: Final[str] = "priority"
TYPE: Final[str] = "type"
PATTERN: Final[str] = "pattern"
DESTINATION: Final[str] = "destination"

# default values
DEFAULT_EXCLUSION_FOLDER_NAME: Final[str] = "exclusion_queue"
DEFAULT_CLEANUP_LOG_NAME: Final[str] = "cleanup_log.txt"
DEFAULT_MOVE_DELAY: Final[int] = 30
DEFAULT_EXCLUSION_DELAY: Final[int] = 60
DEFAULT_CLEANUP_SETTINGS_FILE: Final[str] = str(Path(__file__).parent.parent / "cleanup_settings.json")
DEFAULT_SETTINGS: dict[str, Any] = {
    CLEANUP_FOLDER_PATH: str(Path.home() / "Downloads"),
    MOVE_DELAY: DEFAULT_MOVE_DELAY,
    EXCLUSION_DELAY: DEFAULT_EXCLUSION_DELAY,
    SHOULD_MOVE_FOLDER: False,
    EXCLUSION_FOLDER_NAME: DEFAULT_EXCLUSION_FOLDER_NAME,
    CLEANUP_LOG_NAME: DEFAULT_CLEANUP_LOG_NAME,
    UNMATCHED_FILE_ACTION: UnmatchedFileActionEnum.KEEP.value,
    ORGANIZATION_RULES: [
        {
            PRIORITY: 1,
            TYPE: OrganizationTypeEnum.EXTENSION.value,
            PATTERN: ".pdf",
            DESTINATION: str(Path.home() / "Documents" / "pdfs"),
        }
    ],
}
