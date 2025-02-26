import logging
from app.config import settings

class Logger:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logger = cls._setup_logger()
        return cls._instance

    @classmethod
    def _setup_logger(cls):
        """
        Initializes and configures the logger with a console handler.
        """
        logger = logging.getLogger("app_logger")
        log_level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
        logger.setLevel(log_level)

        if not logger.hasHandlers():  # Avoid adding duplicate handlers
            cls._setup_console_logger(logger)

        return logger

    @staticmethod
    def _setup_console_logger(logger):
        """
        Configures and adds a console handler to the logger.
        """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    def get_logger(self):
        """
        Returns the singleton logger instance.
        """
        return self.logger

# Create a global singleton logger instance
logger = Logger().get_logger()
