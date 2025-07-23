"""Service for loading cleanup job configurations from the settings file."""

import json
from typing import List

from constant.file_constants import (
    CLEANUP_SETTINGS_FILE,
    DEFAULT_SETTINGS,
    READ_COMMAND,
    WRITE_COMMAND,
    STANDARD_ENCODING,
)
from model.cleanup_job import CleanupJob


def get_cleanup_jobs() -> List[CleanupJob]:
    """
    Loads all cleanup job configurations from the settings file.

    Returns:
        A list of CleanupJob objects, one for each configuration found.
    """
    cleanup_jobs = []

    try:
        with open(
            CLEANUP_SETTINGS_FILE, READ_COMMAND, encoding=STANDARD_ENCODING
        ) as settings_file:
            all_configs = json.load(settings_file)

            if isinstance(all_configs, list):
                for config in all_configs:
                    try:
                        cleanup_jobs.append(CleanupJob(config))
                    except ValueError as e:
                        print(f"Skipping invalid job config: {e}. Config was: {config}")
            else:
                print(
                    "Warning: 'cleanup_settings.json' should contain a list of job objects."
                )

    except FileNotFoundError:
        print(
            f"Settings file '{CLEANUP_SETTINGS_FILE}' not found. Creating with a default example."
        )
        _create_default_settings_file()
    except json.JSONDecodeError:
        print(
            f"Error decoding JSON from '{CLEANUP_SETTINGS_FILE}'. Please check its format."
        )

    return cleanup_jobs


def _create_default_settings_file() -> None:
    """Creates a default settings file with one example job."""
    with open(
        CLEANUP_SETTINGS_FILE, WRITE_COMMAND, encoding=STANDARD_ENCODING
    ) as settings_file:
        json.dump([DEFAULT_SETTINGS], settings_file, indent=4)
