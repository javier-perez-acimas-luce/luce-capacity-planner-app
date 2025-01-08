import logging
from datetime import datetime

from pytz import timezone as tz

from app_name.utils import io


class LogManager:
    _MSG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    _DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    _LOG_PATH = None

    def __init__(self, name, level='INFO', timezone='UTC', persist=False):
        """
        Initialize the LogManager with a logger name, log level, and timezone.

        Args:
            name (str): The name of the logger.
            level (str): The log level for the logger (default is 'INFO').
            timezone (str): The timezone for the logger (default is 'UTC').
        """
        self.timezone = timezone
        self.name = name
        self.logger = self._get_logger(name, level, persist)

    def _get_logger(self, name, level, persist):
        """
        Create and configure a logger with the specified name, log level, and timezone.

        Args:
            name (str): The name of the logger.
            level (str): The log level for the logger.

        Returns:
            logging.Logger: The configured logger.
        """
        logger = logging.getLogger(name)
        logger = self._set_loglevel(logger, level)
        formatter = logging.Formatter(self._MSG_FORMAT, datefmt=self._DATETIME_FORMAT)
        formatter.converter = self._time_converter
        handler = self._create_handler(formatter)
        logger = self._add_handler(logger, handler)
        if persist:
            file_handler = self._create_handler(formatter, type='file')
            logger = self._add_handler(logger, file_handler)
        return logger

    def _create_handler(self, formatter, type='screen'):
        """
        Create a logging handler with the specified formatter.

        Args:
            formatter (logging.Formatter): The formatter to set for the handler.

        Returns:
            logging.Handler: The created logging handler with the specified formatter.
        """
        type = type.lower()
        if type == "screen":
            handler = logging.StreamHandler()
        elif type == "file":
            handler = logging.FileHandler(self.name + ".log", mode="a", encoding="utf-8")
        elif type == "gcp":
            #  TODO: Change the handler creation to allow GCP logging and other logging services.
            raise NotImplementedError("GCP logging is not implemented yet.")
        else:
            handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        return handler

    def _add_handler(self, logger, handler):
        """
        Add a handler to the specified logger.

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

    def _time_converter(self, *args):
        """
        Convert the time to the specified timezone.

        Returns:
            time.struct_time: The converted time.
        """
        utc_dt = datetime.now(tz('UTC'))
        local_dt = utc_dt.astimezone(tz(self.timezone))
        return local_dt.timetuple()

    def get_logger(self):
        """
        Get the configured logger.

        Returns:
            logging.Logger: The configured logger.
        """
        return self.logger


config = io.load_config_by_env()
log_level = io.fetch_env_variable(config, 'LOG_LEVEL')
timezone = io.fetch_env_variable(config, 'LOG_TIMEZONE')
logger = LogManager(name="app_name", level=log_level, timezone=timezone, persist=False).get_logger()
