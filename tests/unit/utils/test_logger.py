import logging

import pytest

from app_name.utils.logger import LogManager, log


@pytest.fixture
def log_manager():
    return LogManager(name="test_logger", level="DEBUG", timezone="UTC", deep_log=0, persist=False)


def test_log_manager_initialization(log_manager):
    assert log_manager.name == "test_logger"
    assert log_manager.timezone == "UTC"
    assert isinstance(log_manager.logger, logging.Logger)


def test_log_manager_set_loglevel(log_manager):
    logger = log_manager._set_loglevel(log_manager.logger, "INFO")
    assert logger.level == logging.INFO


def test_log_manager_create_handler_screen(log_manager):
    handler = log_manager._create_handler(logging.Formatter(), type="screen")
    assert isinstance(handler, logging.StreamHandler)


def test_log_manager_create_handler_file(log_manager):
    handler = log_manager._create_handler(logging.Formatter(), type="file")
    assert isinstance(handler, logging.FileHandler)


def test_log_manager_add_handler(log_manager):
    handler = logging.StreamHandler()
    logger = log_manager._add_handler(log_manager.logger, handler)
    assert handler in logger.handlers


def test_log_manager_time_converter(log_manager):
    time_tuple = log_manager._time_converter()
    assert isinstance(time_tuple, tuple)


def test_log(mocker):
    mock_machine_stats = mocker.patch('app_name.utils.logger.machine_stats')
    mock_machine_stats.stats_to_message.return_value = '{"cpu_count": "4 cores"}'
    message = log("Test message")
    assert "Test message" in message
    assert "Stats" in message
