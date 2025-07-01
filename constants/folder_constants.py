import os

DOWNLOADS_FOLDER_NAME: str = "Downloads"
EXCLUSION_FOLDER_NAME: str = "exclusion_queue"
CLEANUP_TXT_NAME: str      = "cleanup_log.txt"
DOWNLOADS_PATH: str        = os.path.expanduser(f"~/{DOWNLOADS_FOLDER_NAME}")
EXCLUSION_QUEUE_PATH: str  = os.path.join(DOWNLOADS_PATH, EXCLUSION_FOLDER_NAME)
LOG_PATH: str              = os.path.join(EXCLUSION_QUEUE_PATH, CLEANUP_TXT_NAME)
