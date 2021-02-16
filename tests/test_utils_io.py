
import re
import pytest

from src.utils import io

def test_load_config_raises_exception(root_dir):
    with pytest.raises(FileNotFoundError):
        result = io.load_config(root_dir + "fake_file")

def test_load_config(root_dir):
    result = io.load_config(root_dir+"config.yaml")
    assert result is not None

def test_is_key_in_config_file_raises_exception():
    with pytest.raises(Exception):
        io.is_key_in_config_file(None, "test_key")

def test_fetch_env_variable_raises_error_when_not_set(config):
    with pytest.raises(KeyError):
        io.fetch_env_variable(config, "FAKE", None)

def test_fetch_env_variable_raises_error_when_group_not_set(config):
    with pytest.raises(KeyError):
        io.fetch_env_variable(config, "token", "group")

def test_fetch_env_variable_raises_error_when_group_not_set(config):
    result = io.fetch_env_variable(config, "token", None)
    assert result is not None and result!=""

def test_get_date_sub_path_returns_correct_path(config):
    result = io.get_date_sub_path("myfile")
    result = re.match(r'\d+/\d+/\d+/myfile', result)
    assert result is not None
