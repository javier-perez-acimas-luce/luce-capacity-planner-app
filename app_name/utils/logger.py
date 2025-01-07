# To use logger in other modules:
# from app_name.utils.logger import logger
# logger.debug("This is a debug message")
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is a error message")
# logger.critical("This is a critical message")

import logging

from app_name.utils import io


class LogManager:
    def __init__(self, name, level='INFO'):
        """
        Initialize the LogManager with a logger name and log level.

        Args:
            name (str): The name of the logger.
            level (str): The log level for the logger (default is 'info').
        """
        self.logger = self._get_logger(name, level)

    def _get_logger(self, name, level):
        """
        Create and configure a logger with the specified name and log level.

        Args:
            name (str): The name of the logger.
            level (str): The log level for the logger.

        Returns:
            logging.Logger: The configured logger.
        """
        logger = logging.getLogger(name)
        logger = self._set_loglevel(logger, level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        return logger

    def _set_loglevel(self, logger, level):
        """
        Set the log level for the specified logger.

        Args:
            logger (logging.Logger): The logger to set the level for.
            level (str): The log level to set.

        Returns:
            logging.Logger: The logger with the updated log level.
        """
        level = level.upper()
        level_mapping = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'INFORMATION': logging.INFO,
            'WARN': logging.WARNING,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        if level not in level_mapping:
            logger.error(f"Invalid log level: {level}. Log level set to INFO.")
        logger.setLevel(level_mapping.get(level, logging.INFO))
        return logger

    def get_logger(self):
        """
        Get the configured logger.

        Returns:
            logging.Logger: The configured logger.
        """
        return self.logger


config = io.load_config_by_env()
log_level = io.fetch_env_variable(config, 'LOG_LEVEL')
logger = LogManager(name="app_name", level=log_level).get_logger()
