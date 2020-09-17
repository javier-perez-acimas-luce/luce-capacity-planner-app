import pytest
import src.example.module as mod

def test_do_something_returns_true(config_file, mocker):
    m = mocker.patch('src.example.module.write_output_file')
    result = mod.do_something(config_file)
    assert result is True