"""Main script for cleaning up the specified folder by moving and deleting old files.

This script moves files older than X days from the specified directory to an exclusion queue,
and deletes files older than Y days from the exclusion queue. Logging is performed for all actions.
"""

import os
from datetime import (
    datetime,
)

from service.cleanup_service import delete_files, move_files
from service.logger_service import write_log
from service.settings_service import get_settings


# todo: add anacron tab
# todo: add windows support
# todo: fill 'about' section

def main() -> None:
    """Run the main cleanup process by moving and deleting old files."""
    settings = get_settings()
    os.makedirs(settings.exclusion_queue_path, exist_ok=True)

    write_log(f"=== Starting Cleanup Process: {datetime.now().strftime('%Y-%m-%d')} ===")

    moved_count: int = move_files(settings)
    deleted_count: int = delete_files(settings)

    write_log(f"Moved {moved_count} files to {settings.exclusion_folder_name}")
    write_log(f"Deleted {deleted_count} files/folders from {settings.exclusion_folder_name}")
    write_log("=== Cleanup Process Completed ===\n")


if __name__ == "__main__":
    main()
