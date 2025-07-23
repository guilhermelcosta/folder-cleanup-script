"""Constants for file operation modes and standard encoding."""

READ_COMMAND: str = "r"
APPEND_COMMAND: str = "a"
WRITE_COMMAND: str = "w"
STANDARD_ENCODING: str = "utf-8"
CLEANUP_SETTINGS_FILE: str = "cleanup_settings.json"
DEFAULT_SETTINGS: dict = {
    "cleanup_folder_path": "/path/to/your/downloads",
    "move_delay": 30,
    "exclusion_delay": 60,
    "should_move_folder": False,
    "exclusion_folder_name": "exclusion_queue",
    "cleanup_log_name": "cleanup_log.txt",
    "unmatched_file_action": "keep",
    "organization_rules": [
        {
            "priority": 1,
            "type": "extension",
            "pattern": ".pdf",
            "destination": "/path/to/your/documents/pdfs",
        }
    ],
}
