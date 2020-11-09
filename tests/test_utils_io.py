import pytest

from src.utils import io

def test_load_config_raises_esception(root_dir):
    with pytest.raises(FileNotFoundError):
        result = io.load_config(root_dir + "fake_file")

def test_load_config(root_dir):
    result = io.load_config(root_dir+"config.yaml")
    assert result is not None

def test_is_key_in_config_file_raises_exception():
    with pytest.raises(Exception):
        io.is_key_in_config_file(None, "test_key")

def test_is_key_in_config_file_finds_key(config):
    result = io.is_key_in_config_file(config, "GOOGLE_APPLICATION_CREDENTIALS")
    assert result is True

def test_fetch_env_variable_raises_error_when_not_set(config):
    with pytest.raises(KeyError):
        io.fetch_env_variable(config, "FAKE", None)

def test_fetch_env_variable_raises_error_when_group_not_set(config):
    with pytest.raises(KeyError):
        io.fetch_env_variable(config, "GOOGLE_APPLICATION_CREDENTIALS", "group")

def test_fetch_env_variable_raises_error_when_group_not_set(config):
    result = io.fetch_env_variable(config, "GOOGLE_APPLICATION_CREDENTIALS", None)
    assert result is not None and result!=""


