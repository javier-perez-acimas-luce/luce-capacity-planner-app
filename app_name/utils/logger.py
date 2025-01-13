import logging
import os
from datetime import datetime

from pytz import timezone as tz

from app_name.utils import io
from app_name.utils.machine_stats import machine_stats


class LogManager:
    """
    LogManager is responsible for setting up and managing the logging configuration for the application.

    Attributes:
        timezone (str): The timezone to use for log timestamps.
        name (str): The name of the logger.
        logger (logging.Logger): The configured logger instance.
    """
    _MSG_FORMAT = '%(asctime)s.%(msecs)d - %(name)s - ' + str(
        os.getpid()) + ' - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
    _MSG_FORMAT_EXTENDED = '#Timestamp: %(asctime)s.%(msecs)d - #Logger_name: %(name)s - #PID: ' + str(
        os.getpid()) + ' - #Log_level: %(levelname)s - #Source_path: %(pathname)s:%(lineno)d - #Function: %(funcName)s() - #Thread: [%(thread)d] %(threadName)s - #Task: %(taskName)s - #Process: %(process)d - #Message: %(message)s'
    _DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    _LOG_PATH = None

    def __init__(self, name, level='INFO', timezone='UTC', deep_log=0, persist=False):
        """
        Initializes the LogManager with the given parameters.

        Args:
            name (str): The name of the logger.
            level (str): The logging level (default is 'INFO').
            timezone (str): The timezone for log timestamps (default is 'UTC').
            deep_log (int): Flag to activate deep logging (default is 0).
            persist (bool): Flag to enable logging to a file (default is False).
        """
        self.timezone = timezone
        self.name = name
        self.logger = self._get_logger(name, level, deep_log, persist)

    def _get_logger(self, name, level, deep_log, persist):
        """
        Configures and returns a logger instance.

        Args:
            name (str): The name of the logger.
            level (str): The logging level.
            deep_log (int): Flag to activate deep logging.
            persist (bool): Flag to enable logging to a file.

        Returns:
            logging.Logger: The configured logger instance.
        """
        logger = logging.getLogger(name)
        logger = self._set_loglevel(logger, level)
        if deep_log == 0:
            formatter = logging.Formatter(self._MSG_FORMAT, datefmt=self._DATETIME_FORMAT)
        else:
            formatter = logging.Formatter(self._MSG_FORMAT_EXTENDED, datefmt=self._DATETIME_FORMAT)
        formatter.converter = self._time_converter
        handler = self._create_handler(formatter)
        logger = self._add_handler(logger, handler)
        if persist:
            file_handler = self._create_handler(formatter, type='file')
            logger = self._add_handler(logger, file_handler)
        return logger

    def _create_handler(self, formatter, type='screen'):
        """
        Creates and returns a logging handler.

        Args:
            formatter (logging.Formatter): The formatter to use for the handler.
            type (str): The type of handler ('screen' or 'file').

        Returns:
            logging.Handler: The configured logging handler.
        """
        type = type.lower()
        if type == "screen":
            handler = logging.StreamHandler()
        elif type == "file":
            handler = logging.FileHandler(self.name + ".log", mode="a", encoding="utf-8")
        elif type == "gcp":
            raise NotImplementedError("GCP logging is not implemented yet.")
        else:
            handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        return handler

    def _add_handler(self, logger, handler):
        """
        Adds a handler to the logger.

        Args:
            logger (logging.Logger): The logger to add the handler to.
            handler (logging.Handler): The handler to add.

        Returns:
            logging.Logger: The logger with the added handler.
        """
        logger.addHandler(handler)
        return logger

    def _set_loglevel(self, logger, level):
        """
        Sets the logging level for the logger.

        Args:
            logger (logging.Logger): The logger to set the level for.
            level (str): The logging level.

        Returns:
            logging.Logger: The logger with the set level.
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

    def _time_converter(self, *args):
        """
        Converts the current time to the specified timezone.

        Returns:
            time.struct_time: The converted time.
        """
        utc_dt = datetime.now(tz('UTC'))
        local_dt = utc_dt.astimezone(tz(self.timezone))
        return local_dt.timetuple()

    def get_logger(self):
        """
        Returns the configured logger instance.

        Returns:
            logging.Logger: The configured logger instance.
        """
        return self.logger


def log(message, stats_units='GB'):
    """
    Appends machine stats to the log message.

    Args:
        message (str): The log message.
        stats_units (str): The units for the machine stats (default is 'GB').

    Returns:
        str: The log message with appended machine stats.
    """
    return message + " - Stats: " + machine_stats.stats_to_message(stats_units)


config = io.load_config_by_env()
try:
    log_level = io.fetch_env_variable(config, 'LOG_LEVEL')
except KeyError:
    log_level = 'INFO'
try:
    timezone = io.fetch_env_variable(config, 'LOG_TIMEZONE')
except KeyError:
    timezone = 'UTC'
try:
    deep_log = io.fetch_env_variable(config, 'DEEP_LOG')
except KeyError:
    deep_log = 0

logger = LogManager(name="app_name", level=log_level, timezone=timezone, deep_log=deep_log, persist=False).get_logger()