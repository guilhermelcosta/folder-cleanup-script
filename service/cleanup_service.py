"""Service module for moving and deleting old files based on configurable settings.

This module provides functions to move files older than a specified delay from a cleanup folder
to an exclusion queue, and to delete files from the exclusion queue after another delay.
"""

import os
import shutil
import time

from constant.time_constants import HOURS_IN_ONE_DAY, MINUTES_IN_ONE_HOUR, SECONDS_IN_ONE_MINUTE
from model.settings import Settings
from service.logger_service import write_log


def move_files(settings: Settings) -> int:
    """Move files older than X days from the cleanup folder to the exclusion queue.

    Scans the cleanup folder for files and (optionally) folders. For each item that has not been accessed
    in the last X days, moves it to the exclusion queue directory. If a name conflict occurs in the
    destination, appends a numeric suffix to the filename to avoid overwriting. Logs each move and any errors.

    Args:
        settings (Settings): The configuration settings for the cleanup operation.

    Returns:
        int: The number of files or folders moved.

    """
    moved_count = 0
    now = time.time()
    move_delay = _convert_days_to_seconds(int(settings.move_delay))

    for filename in os.listdir(settings.cleanup_folder_path):
        file_path = os.path.join(settings.cleanup_folder_path, filename)
        is_folder = os.path.isdir(file_path)

        if (not settings.should_move_folder and is_folder) or file_path == settings.exclusion_queue_path:
            continue

        if now - os.path.getatime(file_path) > move_delay:
            destination_path = os.path.join(settings.exclusion_queue_path, filename)
            file_base_name, file_extension = os.path.splitext(filename)
            counter = 1

            while os.path.exists(destination_path):
                if file_extension:
                    destination_path = os.path.join(
                        settings.exclusion_queue_path, f"{file_base_name}({counter}){file_extension}"
                    )
                else:
                    destination_path = os.path.join(settings.exclusion_queue_path, f"{file_base_name}({counter})")
                counter += 1

            try:
                shutil.move(file_path, destination_path)
                write_log(
                    f"Moved: {filename} -> {settings.exclusion_folder_name} ({'folder' if is_folder else 'file'})"
                )

                moved_count += 1
            except Exception as e:
                write_log(f"Error while moving {filename}: {e}")

    return moved_count


def delete_files(settings: Settings) -> int:
    """Delete files or folders older than X days from the exclusion queue directory.

    Scans the exclusion queue directory for files and (optionally) folders. For each item that has not been accessed
    in the last X days, deletes it. Logs each deletion and any errors encountered. Skips folders if configured not to move folders,
    and skips the cleanup log file. Logs the total number of files or folders deleted and marks the completion of the cleanup process.

    Args:
        settings (Settings): The configuration settings for the cleanup operation.

    Returns:
        int: The number of files or folders deleted.

    """
    deleted_count = 0
    exclusion_delay = _convert_days_to_seconds(int(settings.exclusion_delay))
    now = time.time()

    for filename in os.listdir(settings.exclusion_queue_path):
        file_path = os.path.join(settings.exclusion_queue_path, filename)
        is_folder = os.path.isdir(file_path)

        if (not settings.should_move_folder and is_folder) or filename == settings.cleanup_log_name:
            continue

        if now - os.path.getatime(file_path) > exclusion_delay:
            try:
                if is_folder:
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)

                write_log(f"Deleted: {filename} ({'folder' if is_folder else 'file'})")

                deleted_count += 1
            except Exception as e:
                write_log(f"Error deleting {filename}: {e}")

    write_log("---")

    return deleted_count


def _convert_days_to_seconds(days: int) -> int:
    """Convert a given number of days to the equivalent number of seconds.

    Args:
        days (int): The number of days to convert.

    Returns:
        int: The total number of seconds in the specified number of days.

    """
    return days * HOURS_IN_ONE_DAY * MINUTES_IN_ONE_HOUR * SECONDS_IN_ONE_MINUTE
