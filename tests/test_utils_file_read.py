import pytest

from src.utils import read_file as fru


def test_get_date_sub_path_raises_exception_when_invalid_date():
    with pytest.raises(AttributeError):
        fru.get_date_sub_path("test")


def test_get_date_sub_path_gets_path(etl_date):
    path = fru.get_date_sub_path(etl_date)
    assert path == '2019/201907/20190716/'


def test_load_config_raises_esception(root_dir):
    with pytest.raises(FileNotFoundError):
        result = fru.load_config(root_dir + "fake_file")


def test_load_config(root_dir):
    result = fru.load_config(root_dir+"config.yml")
    assert result is not None


def test_is_key_in_config_file_raises_exception():
    with pytest.raises(Exception):
        fru.is_key_in_config_file(None, "test_key")


def test_is_key_in_config_file_finds_key(config_file):
    result = fru.is_key_in_config_file(config_file, "datalake", ['input_path'])
    assert result is True


def test_is_key_in_config_file_fails_key(config_file):
    result = fru.is_key_in_config_file(config_file, "test_key", ['path'])
    assert result is False


def test_is_key_in_config_file_fails_value(config_file):
    result = fru.is_key_in_config_file(config_file, "datalake", ['test_value', 'input_path'])
    assert result is False