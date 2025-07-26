from datetime import datetime

from constants.constants import APPEND_COMMAND, STANDARD_ENCODING


def write_log(message: str, log_path: str | None = None) -> None:
    """Write a log message to a specified log file and print it to the console.

    Args:
        message (str): The message to be logged.
        log_path (str, optional): The full path to the log file. If None, message is only printed to the console.

    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} - {message}"

    if log_path:
        try:
            with open(log_path, APPEND_COMMAND, encoding=STANDARD_ENCODING) as log_file:
                log_file.write(log_message + "\n")
        except Exception as e:
            print(f"CRITICAL: Could not write to log file '{log_path}'. Error: {e}")

    print(log_message)
