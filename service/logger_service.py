"""Logger service for writing timestamped log messages to a file and printing them to the console."""

from datetime import datetime

from constant.file_constants import APPEND_COMMAND, STANDARD_ENCODING
from constant.folder_constants import LOG_PATH


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
