"""Main script for cleaning up multiple specified folders by organizing, moving, and deleting old files.

This script reads a list of cleanup jobs from a settings file. For each job, it first
organizes files based on rules, then moves files older than X days to an exclusion queue,
and finally deletes files older than Y days from the exclusion queue.

Logging is performed for all actions, potentially to a unique log file for each job.
"""

import os
from datetime import datetime

from model.cleanup_job import CleanupJob
from service.cleanup_service import delete_files, move_files, organize_files
from service.logger_service import write_log
from service.settings_service import get_cleanup_jobs


def main() -> None:
    """Run the main cleanup process for all configured jobs."""
    cleanup_jobs: list[CleanupJob] = get_cleanup_jobs()

    if not cleanup_jobs:
        print("No cleanup jobs found in 'cleanup_settings.json'. Exiting.")
        return

    for job in cleanup_jobs:
        try:
            write_log(
                f"=== Starting Cleanup: '{job.cleanup_folder_path}' ({datetime.now().strftime('%Y-%m-%d')}) ===",
                job.cleanup_log_path,
            )

            os.makedirs(job.cleanup_folder_path, exist_ok=True)
            os.makedirs(job.exclusion_queue_path, exist_ok=True)

            for rule in job.organization_rules:
                destination = rule.get("destination")
                if destination:
                    os.makedirs(destination, exist_ok=True)

            organized_count, organized_files = organize_files(job)
            write_log(
                f"Organized {organized_count} files into specific folders.",
                job.cleanup_log_path,
            )

            moved_count = 0

            if job.unmatched_file_action == "delete":
                moved_count = move_files(job, organized_files)

                write_log(
                    f"Moved {moved_count} files to '{job.exclusion_folder_name}'.",
                    job.cleanup_log_path,
                )
            else:
                write_log(
                    "Skipping move phase for unmatched files as per settings ('keep').",
                    job.cleanup_log_path,
                )

            deleted_count = delete_files(job)

            write_log(
                f"Deleted {deleted_count} files/folders from '{job.exclusion_folder_name}'.",
                job.cleanup_log_path,
            )
            write_log(
                f"=== Completed Cleanup: '{job.cleanup_folder_path}' ===\n",
                job.cleanup_log_path,
            )

        except Exception as e:
            error_message = f"!!! An unexpected error occurred while processing job for '{job.cleanup_folder_path}': {e} !!!"

            try:
                write_log(error_message, job.cleanup_log_path)
            except Exception:
                print(error_message)


if __name__ == "__main__":
    main()
