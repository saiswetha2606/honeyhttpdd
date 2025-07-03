# honeyhttpd/loggers/FileLogger.py

import datetime
import os

class FileLogger:
    def __init__(self, config=None):
        if config is None:
            config = {}
        self.log_file = config.get("log_file", "./logs/honeyhttpd.log")
        self.log_level = config.get("log_level", "info").lower()

        # Ensure the log directory exists
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def stores_large(self):
        # Return False because this logger does not store large amounts of data
        return False

    def log(self, remote_ip, remote_port, is_ssl, port, request, response, extra={}):
        protocol = "https" if is_ssl else "http"
        now = datetime.datetime.now().isoformat()
        log_entry = (
            f"\n{now} - From {remote_ip}:{remote_port} via {protocol} port {port}:\n"
            f"Request:\n{request}\n"
            f"Response:\n{response}\n"
        )
        # Append log entry to the log file
        with open(self.log_file, "a") as output_file:
            output_file.write(log_entry)
