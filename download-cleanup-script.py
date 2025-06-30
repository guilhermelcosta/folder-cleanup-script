import os
import shutil
import time
from datetime import datetime

DOWNLOADS_PATH = os.path.expanduser("~/Downloads")
EXCLUSION_QUEUE_PATH = os.path.join(DOWNLOADS_PATH, "exclusion_queue")
LOG_PATH = os.path.join(EXCLUSION_QUEUE_PATH, "cleanup_log.txt")

def main():

    # Create exclusion_queue folder if it doesn't exist
    os.makedirs(EXCLUSION_QUEUE_PATH, exist_ok=True)
    write_log(f"Created exclusion_queue folder: {EXCLUSION_QUEUE_PATH}")
    write_log("=== Starting Downloads Cleanup Process ===")
    write_log("Moving files older than 30 days from Downloads to exclusion_queue")

    move_files    
    write_log("Deleting files older than 60 days from exclusion_queue")
    delete_old_files


def write_log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} - {message}"
    with open(LOG_PATH, "a") as log_file:
        log_file.write(log_message + "\n")
    print(log_message)

def move_files():
    moved_count = 0
    now = time.time()
    # days_30 = 30 * 24 * 60 * 60
    days_30 = 30 

    for filename in os.listdir(DOWNLOADS_PATH):
        file_path = os.path.join(DOWNLOADS_PATH, filename)
        if not os.path.isfile(file_path):
            continue
        # if filename == "cleanup_log.txt":
        #     continue
        
        if now - os.path.getatime(file_path) > days_30:
            dest_path = os.path.join(EXCLUSION_QUEUE_PATH, filename)
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                if ext:
                    dest_path = os.path.join(EXCLUSION_QUEUE_PATH, f"{base}({counter}){ext}")
                else:
                    dest_path = os.path.join(EXCLUSION_QUEUE_PATH, f"{base}({counter})")
                counter += 1
            try:
                shutil.move(file_path, dest_path)
                write_log(f"Moved: {filename} -> exclusion_queue")
                moved_count += 1
            except Exception as e:
                write_log(f"Error moving {filename}: {e}")

    write_log(f"Successfully moved {moved_count} files to exclusion_queue")

def delete_old_files():
    deleted_count = 0
    days_60 = 60

    for filename in os.listdir(EXCLUSION_QUEUE_PATH):
        file_path = os.path.join(EXCLUSION_QUEUE_PATH, filename)
        if not os.path.isfile(file_path):
            continue
        if now - os.path.getatime(file_path) > days_60:
            try:
                os.remove(file_path)
                write_log(f"Deleted: {filename}")
                deleted_count += 1
            except Exception as e:
                write_log(f"Error deleting {filename}: {e}")

    write_log(f"Successfully deleted {deleted_count} files from exclusion_queue")
    write_log("=== Downloads Cleanup Process Completed ===")
    write_log("")

if __name__ == "__main__":
    main()
