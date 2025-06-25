#!/bin/bash

# Downloads Folder Cleanup Script for WSL
# This script moves old files to exclusion_queue and deletes very old files

# Configuration - Windows paths accessible from WSL
DOWNLOADS_PATH="/mnt/c/Users/Guilherme/Downloads"
EXCLUSION_QUEUE_PATH="/mnt/c/Users/Guilherme/Downloads/exclusion_queue"
LOG_PATH="/mnt/c/Users/Guilherme/Downloads/cleanup_log.txt"

# Check if Windows username is different from WSL username
if [ ! -d "$DOWNLOADS_PATH" ]; then
    echo "Downloads folder not found at $DOWNLOADS_PATH"
    echo "Please check your Windows username and update the script accordingly"
    echo "Your WSL username is: $USER"
    echo "Try: ls /mnt/c/Users/ to see available Windows user folders"
    exit 1
fi

# Create exclusion_queue folder if it doesn't exist
if [ ! -d "$EXCLUSION_QUEUE_PATH" ]; then
    mkdir -p "$EXCLUSION_QUEUE_PATH"
    echo "Created exclusion_queue folder: $EXCLUSION_QUEUE_PATH"
fi

# Function to log messages
write_log() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_message="$timestamp - $message"
    echo "$log_message" >> "$LOG_PATH"
    echo "$log_message"
}

write_log "=== Starting Downloads Cleanup Process ==="

# Step 1: Move files older than 1 month from Downloads to exclusion_queue
write_log "Moving files older than 30 days from Downloads to exclusion_queue"

moved_count=0
# Find files older than 30 days (excluding the log file and exclusion_queue folder)
find "$DOWNLOADS_PATH" -maxdepth 1 -type f -name "*.pdf" -o -name "*.jpg" -o -name "*.png" -o -name "*.doc*" -o -name "*.zip" -o -name "*.exe" -o -name "*.mp4" -o -name "*.mp3" -o -name "*.*" | while read -r file; do
    # Skip the log file
    if [[ "$(basename "$file")" == "cleanup_log.txt" ]]; then
        continue
    fi
    
    # Check if file is older than 30 days using access time
    if [[ $(find "$file" -atime +30 2>/dev/null) ]]; then
        filename=$(basename "$file")
        destination="$EXCLUSION_QUEUE_PATH/$filename"
        
        # Handle duplicate names
        counter=1
        while [ -f "$destination" ]; do
            filename_no_ext="${filename%.*}"
            extension="${filename##*.}"
            if [ "$filename_no_ext" = "$filename" ]; then
                # No extension
                destination="$EXCLUSION_QUEUE_PATH/${filename}($counter)"
            else
                destination="$EXCLUSION_QUEUE_PATH/${filename_no_ext}($counter).$extension"
            fi
            ((counter++))
        done
        
        if mv "$file" "$destination" 2>/dev/null; then
            write_log "Moved: $filename -> exclusion_queue"
            ((moved_count++))
        else
            write_log "Error moving $filename"
        fi
    fi
done

write_log "Successfully moved $moved_count files to exclusion_queue"

# Step 2: Delete files older than 2 months from exclusion_queue
write_log "Deleting files older than 60 days from exclusion_queue"

deleted_count=0
# Find files older than 60 days in exclusion_queue
find "$EXCLUSION_QUEUE_PATH" -type f -atime +60 2>/dev/null | while read -r file; do
    filename=$(basename "$file")
    if rm "$file" 2>/dev/null; then
        write_log "Deleted: $filename"
        ((deleted_count++))
    else
        write_log "Error deleting $filename"
    fi
done

write_log "Successfully deleted $deleted_count files from exclusion_queue"
write_log "=== Downloads Cleanup Process Completed ==="
write_log ""
