"""Constants for folder and file paths used in the download cleanup script."""

import os

DEFAULT_CLEANUP_FOLDER_NAME: str = "Downloads"
DEFAULT_EXCLUSION_FOLDER_NAME: str = "exclusion_queue"
DEFAULT_CLEANUP_LOG_NAME: str = "cleanup_log.txt"
DOWNLOADS_PATH: str = os.path.expanduser(f"~/{DEFAULT_CLEANUP_FOLDER_NAME}")
EXCLUSION_QUEUE_PATH: str = os.path.join(DOWNLOADS_PATH, DEFAULT_EXCLUSION_FOLDER_NAME)
LOG_PATH: str = os.path.join(EXCLUSION_QUEUE_PATH, DEFAULT_CLEANUP_LOG_NAME)
