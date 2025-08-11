import logging
import sys
import os
from datetime import datetime
from colorama import Fore, Style

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, Fore.WHITE)
        log_fmt = f"{log_color}%(asctime)s - %(levelname)s - %(message)s{Style.RESET_ALL}"
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


class AppLogger:
    _logger = None

    @classmethod
    def get_logger(cls):
        if cls._logger:
            return cls._logger

        # Create logs directory if not exists
        log_dir = os.path.join("app", "logs")
        os.makedirs(log_dir, exist_ok=True)

        # File name will be today's date
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

        logger = logging.getLogger("CodeAnalyser")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        logger.handlers.clear()  # avoid duplicates

        # Console handler (colored)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColorFormatter())

        # File handler (non-colored, daily file)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
        ))

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        cls._logger = logger
        return logger
