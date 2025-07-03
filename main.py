"""Main script for cleaning up the Downloads folder by moving and deleting old files.

This script moves files older than 30 days from the Downloads directory to an exclusion queue,
and deletes files older than 60 days from the exclusion queue. Logging is performed for all actions.
"""

import os
import shutil
import time
from datetime import (
    datetime,
)

from constants.file_constants import (
    APPEND_COMMAND,
    STANDARD_ENCODING,
)
from constants.folder_constants import (
    CLEANUP_TXT_NAME,
    DOWNLOADS_PATH,
    EXCLUSION_FOLDER_NAME,
    EXCLUSION_QUEUE_PATH,
    LOG_PATH,
)
from constants.time_constants import (
    HOURS_IN_ONE_DAY,
    MINUTES_IN_ONE_HOUR,
    SECONDS_IN_ONE_MINUTE,
)


def main() -> None:
    """Run the main cleanup process by moving and deleting old files."""
    os.makedirs(EXCLUSION_QUEUE_PATH, exist_ok=True)

    write_log(f"=== Starting Downloads Cleanup Process: {datetime.now().strftime('%Y-%m-%d')} ===")

    moved_count = move_files()
    deleted_count = delete_old_files()

    write_log(f"Moved {moved_count} files to {EXCLUSION_FOLDER_NAME}")
    write_log(f"Deleted {deleted_count} files/folders from {EXCLUSION_FOLDER_NAME}")
    write_log("=== Downloads Cleanup Process Completed ===\n")


def write_log(message: str) -> None:
    """Write a log message to a log file with a timestamp and prints it to the console.

    Args:
        message (str): The message to be logged.

    Returns:
        None.

    """
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message: str = f"{timestamp} - {message}"

    with open(LOG_PATH, APPEND_COMMAND, encoding=STANDARD_ENCODING) as log_file:
        log_file.write(log_message + "\n")

    print(log_message)


def _convert_days_to_seconds(days: int) -> int:
    """Convert a given number of days to the equivalent number of seconds.

    Args:
        days (int): The number of days to convert.

    Returns:
        int: The total number of seconds in the specified number of days.

    """
    return days * HOURS_IN_ONE_DAY * MINUTES_IN_ONE_HOUR * SECONDS_IN_ONE_MINUTE


def move_files() -> int:
    """Move files older than 30 days from the Downloads directory to the exclusion queue directory.

    This function scans the DOWNLOADS_PATH directory for files (excluding subdirectories),
    and for each file that has not been accessed in the last 30 days, moves it to the
    EXCLUSION_QUEUE_PATH directory. If a file with the same name already exists in the
    destination, a numeric suffix is appended to the filename to avoid overwriting.
    Logs are written for each moved file and for any errors encountered during the move process.

    Returns:
        None

    """
    moved_count = 0
    now = time.time()
    # move_delay = _convert_days_to_seconds(30)
    move_delay = 30

    for filename in os.listdir(DOWNLOADS_PATH):
        file_path = os.path.join(DOWNLOADS_PATH, filename)

        # todo: decide if we want to move directories as well
        # if not os.path.isfile(file_path) or file_path == EXCLUSION_QUEUE_PATH:
        if file_path == EXCLUSION_QUEUE_PATH:
            continue

        if now - os.path.getatime(file_path) > move_delay:
            destination_path = os.path.join(EXCLUSION_QUEUE_PATH, filename)
            file_base_name, file_extension = os.path.splitext(filename)
            counter = 1

            while os.path.exists(destination_path):
                if file_extension:
                    destination_path = os.path.join(
                        EXCLUSION_QUEUE_PATH, f"{file_base_name}({counter}){file_extension}"
                    )
                else:
                    destination_path = os.path.join(EXCLUSION_QUEUE_PATH, f"{file_base_name}({counter})")
                counter += 1

            try:
                shutil.move(file_path, destination_path)
                write_log(f"Moved: {filename} -> {EXCLUSION_FOLDER_NAME}")

                moved_count += 1
            except Exception as e:
                write_log(f"Error while moving {filename}: {e}")

    return moved_count


def delete_old_files() -> int:
    """Delete files older than 60 days from the exclusion queue directory.

    Iterates through all files in the EXCLUSION_QUEUE_PATH directory, checks their last access time,
    and deletes those that have not been accessed in the last 60 days. Logs each deletion and any errors encountered.
    Also logs the total number of files deleted and marks the completion of the cleanup process.
    """
    deleted_count = 0
    exclusion_delay = 60
    now = time.time()

    for filename in os.listdir(EXCLUSION_QUEUE_PATH):
        file_path = os.path.join(EXCLUSION_QUEUE_PATH, filename)

        # if not os.path.isfile(file_path) or filename == CLEANUP_TXT_NAME:
        if filename == CLEANUP_TXT_NAME:
            continue

        if now - os.path.getatime(file_path) > exclusion_delay:
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)

                write_log(f"Deleted: {filename}")

                deleted_count += 1
            except Exception as e:
                write_log(f"Error deleting {filename}: {e}")

    write_log("---")

    return deleted_count


if __name__ == "__main__":
    main()
