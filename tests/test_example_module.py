import pytest
import src.example.module as mod

def test_do_something_returns_true(config_file):
    result = mod.do_something()
    assert result is True