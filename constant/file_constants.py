"""Constants for file operation modes and standard encoding."""

READ_COMMAND: str = "r"
APPEND_COMMAND: str = "a"
WRITE_COMMAND: str = "w"
STANDARD_ENCODING: str = "utf-8"
CLEANUP_SETTINGS_FILE: str = "cleanup_settings.json"
DEFAULT_SETTINGS: dict[str, int | str | bool] = {
    "move_delay": 30,
    "exclusion_delay": 60,
    "should_move_folder": False,
    "cleanup_folder_name": "Downloads",
    "exclusion_folder_name": "exclusion_queue",
    "cleanup_log_name": "cleanup_log.txt",
}
