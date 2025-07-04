"""Service for managing application settings.

This module provides functions to create and save default settings for the cleanup script.
"""

import json

from constant.file_constants import CLEANUP_SETTINGS_FILE, DEFAULT_SETTINGS, READ_COMMAND, STANDARD_ENCODING
from model.settings import Settings
from service.logger_service import write_log


def get_settings() -> Settings:
    """Load settings from the settings file or create default settings if the file does not exist.

    Returns:
        Settings: The loaded or newly created settings object.

    """
    try:
        with open(CLEANUP_SETTINGS_FILE, READ_COMMAND, encoding=STANDARD_ENCODING) as settings_file:
            settings = Settings(json.load(settings_file))
    except FileNotFoundError:
        write_log(f"Settings file '{CLEANUP_SETTINGS_FILE}' not found. Creating with default settings. \n")

        settings = _create_default_settings()

    return settings


def _create_default_settings() -> Settings:
    """Create and save default settings to the settings file, then return a Settings object.

    Returns:
        Settings: The default settings object.

    """
    default_settings = DEFAULT_SETTINGS
    with open(CLEANUP_SETTINGS_FILE, "w", encoding=STANDARD_ENCODING) as settings_file:
        json.dump(default_settings, settings_file, indent=4)

    return Settings(default_settings)
