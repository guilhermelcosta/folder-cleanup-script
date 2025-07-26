import os
import re
import shutil
import time
from typing import Any

from constants.constants import (
    HOURS_IN_ONE_DAY,
    MAX_PRIORITY,
    MINUTES_IN_ONE_HOUR,
    PIPE_OPERATOR,
    SECONDS_IN_ONE_MINUTE,
)
from constants.default_settings_constants import DESTINATION, PATTERN, PRIORITY, TYPE
from enums.organization_type_enum import OrganizationTypeEnum
from models.cleanup_job import CleanupJob
from services.logger_service import write_log


def organize_files(job: CleanupJob) -> tuple[int, set[str]]:
    """Organizes files in the job's cleanup folder based on its rules.

    Args:
        job (CleanupJob): The cleanup job configuration.

    Returns:
        A tuple containing the count of organized files and a set of their original filenames.

    """
    organized_count: int = 0
    organized_files: set[str] = set()
    rules: list[dict[str, Any]] = sorted(job.organization_rules, key=lambda r: r.get(PRIORITY, MAX_PRIORITY))

    for filename in os.listdir(job.cleanup_folder_path):
        file_path: str = os.path.join(job.cleanup_folder_path, filename)

        # does not organize folders
        if os.path.isdir(file_path):
            continue

        for rule in rules:
            try:
                rule_type: str | None = rule.get(TYPE)
                pattern: str | None = rule.get(PATTERN)
                destination: str | None = rule.get(DESTINATION)

                if not all([rule_type, pattern, destination]):
                    continue

                patterns: list[str] | list[str | None] = (
                    pattern.split(PIPE_OPERATOR)
                    if rule_type == OrganizationTypeEnum.EXTENSION.value and pattern
                    else [pattern]
                )
                match: bool = False

                for p in patterns:
                    if rule_type == OrganizationTypeEnum.EXTENSION.value and filename.lower().endswith(p.lower()):
                        match = True

                        break
                    if rule_type == OrganizationTypeEnum.REGEX.value and p and re.search(p, filename, re.IGNORECASE):
                        match = True

                        break

                if match:
                    _move_with_conflict_resolution(file_path, str(destination))
                    write_log(f"Organized: Moved '{filename}' to '{destination}'", job.cleanup_log_path)

                    organized_count += 1
                    organized_files.add(filename)

                    break
            except Exception as e:
                write_log(f"Error organizing '{filename}' with rule {rule}: {e}", job.cleanup_log_path)

    return organized_count, organized_files


def move_files(job: CleanupJob, already_organized_files: set[str]) -> int:
    """Move old files from the cleanup folder to the exclusion queue.

    Args:
        job (CleanupJob): The cleanup job configuration.
        already_organized_files (Set[str]): A set of filenames that have already been handled.

    Returns:
        The number of files/folders moved.

    """
    moved_count: int = 0
    now: float = time.time()
    move_delay: float = _convert_days_to_seconds(job.move_delay)

    for filename in os.listdir(job.cleanup_folder_path):
        if filename in already_organized_files or filename == job.exclusion_folder_name:
            continue

        file_path = os.path.join(job.cleanup_folder_path, filename)
        is_folder = os.path.isdir(file_path)

        if not job.should_move_folder and is_folder:
            continue

        if now - os.path.getatime(file_path) > move_delay:
            try:
                _move_with_conflict_resolution(file_path, job.exclusion_queue_path)
                log_msg = f"Moved to queue: '{filename}' -> '{job.exclusion_folder_name}' ({'folder' if is_folder else 'file'})"

                write_log(log_msg, job.cleanup_log_path)

                moved_count += 1
            except Exception as e:
                write_log(f"Error moving '{filename}' to queue: {e}", job.cleanup_log_path)

    return moved_count


def delete_files(job: CleanupJob) -> int:
    """Delete old files/folders from the exclusion queue.

    Args:
        job (CleanupJob): The cleanup job configuration.

    Returns:
        The number of files/folders deleted.

    """
    deleted_count: int = 0
    now: float = time.time()
    exclusion_delay: float = _convert_days_to_seconds(job.exclusion_delay)

    if not os.path.exists(job.exclusion_queue_path):
        return 0

    for filename in os.listdir(job.exclusion_queue_path):
        if filename == job.cleanup_log_name:
            continue

        file_path = os.path.join(job.exclusion_queue_path, filename)
        is_folder = os.path.isdir(file_path)

        if now - os.path.getatime(file_path) > exclusion_delay:
            try:
                if is_folder:
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)

                write_log(f"Deleted: '{filename}' ({'folder' if is_folder else 'file'})", job.cleanup_log_path)

                deleted_count += 1
            except Exception as e:
                write_log(f"Error deleting '{filename}': {e}", job.cleanup_log_path)

    return deleted_count


def _move_with_conflict_resolution(source_path: str, destination_folder: str) -> None:
    """Move a file to the destination folder, resolving conflicts by renaming.

    Args:
        source_path (str): The path of the file to move.
        destination_folder (str): The folder to move the file to.

    """
    filename = os.path.basename(source_path)
    destination_path = os.path.join(destination_folder, filename)

    # does not move if source and destination are the same
    if source_path == destination_path:
        return

    file_base_name, file_extension = os.path.splitext(filename)
    counter: int = 1

    while os.path.exists(destination_path):
        new_filename: str = f"{file_base_name}({counter}){file_extension}"
        destination_path: str = os.path.join(destination_folder, new_filename)
        counter += 1

    shutil.move(source_path, destination_path)


def _convert_days_to_seconds(days: int) -> int:
    """Convert a given number of days to seconds.

    Args:
        days (int): The number of days to convert.

    Returns:
        The equivalent number of seconds.

    """
    return days * HOURS_IN_ONE_DAY * MINUTES_IN_ONE_HOUR * SECONDS_IN_ONE_MINUTE
