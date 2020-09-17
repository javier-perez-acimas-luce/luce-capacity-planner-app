"""
    File name: conftest.py
    Author: Teresa Paramo
    Date created: 17/9/2020
    Date last modified: 17/9/2020
    Python Version: 3.6

    Description: Any variables you might need during testing so you don´t have to create them in each test. Session scope means any test can access it anytime.
"""

import os
import pytest
import datetime
import yaml

@pytest.fixture(scope='session')
def etl_date() -> datetime.date:
    """
    Creates a date object to run the tests
    @return: datetime.date
    """
    yield datetime.date(day=16, month=7, year=2019)

@pytest.fixture(scope='session')
def config_file() -> yaml:
    """
    Creates a config file object to run the tests
    @return: YAML object
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = root_dir + '/config.yml'
    cfg = None
    with open(config_path, 'r') as ymlfile:
        loader = yaml.Loader(ymlfile)
        cfg = loader.get_single_data()
    yield cfg


@pytest.fixture(scope='session')
def root_dir() ->str:
    """
    Creates a config file object to run the tests
    @return: YAML object
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    yield root_dir + '/'
