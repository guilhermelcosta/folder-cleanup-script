import os

from constants.default_settings_constants import DESTINATION
from enums.unmatched_file_action_enum import UnmatchedFileActionEnum
from models.cleanup_job import CleanupJob
from services.cleanup_service import delete_files, move_files, organize_files
from services.logger_service import write_log
from services.settings_service import get_cleanup_jobs


# todo: add anacron tab
# todo: add windows support
# todo: fill 'about' section

def main() -> None:
    """Run the main cleanup process for all configured jobs."""
    cleanup_jobs: list[CleanupJob] = get_cleanup_jobs()

    if not cleanup_jobs:
        print("No cleanup jobs found in 'cleanup_settings.json', finishing cleanup process.")

        return

    for job in cleanup_jobs:
        try:
            write_log(f"=== Starting Cleanup: '{job.cleanup_folder_path}'", job.cleanup_log_path)

            os.makedirs(job.cleanup_folder_path, exist_ok=True)
            os.makedirs(job.exclusion_queue_path, exist_ok=True)

            for rule in job.organization_rules:
                destination = rule.get(DESTINATION)

                if destination:
                    os.makedirs(destination, exist_ok=True)

            organized_count, organized_files = organize_files(job)

            write_log(f"Organized count: {organized_count}.", job.cleanup_log_path)

            moved_count: int = 0

            if job.unmatched_file_action == UnmatchedFileActionEnum.DELETE.value:
                moved_count: int = move_files(job, organized_files)

                write_log(f"Moved count: {moved_count} ('{job.exclusion_folder_name}').", job.cleanup_log_path)
            else:
                write_log("Skipping move phase for unmatched files as per settings (KEEP).", job.cleanup_log_path)

            deleted_count: int = delete_files(job)

            write_log(f"Deleted count: {deleted_count} ('{job.exclusion_folder_name}').", job.cleanup_log_path)
            write_log(f"=== Completed Cleanup: '{job.cleanup_folder_path}'\n", job.cleanup_log_path)

        except Exception as e:
            error_message: str = f"CRITICAL: Error occurred while processing job for '{job.cleanup_folder_path}': {e}"

            try:
                write_log(error_message, job.cleanup_log_path)
            except Exception:
                print(error_message)


if __name__ == "__main__":
    main()
