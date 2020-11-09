
import os
import pytest
import datetime
import yaml

import main


@pytest.fixture(scope='session')
def config() -> yaml:
    """
    Creates a config file object to run the tests
    @return: YAML object
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = root_dir + '/config.yaml'
    cfg = None
    with open(config_path, 'r') as ymlfile:
        loader = yaml.Loader(ymlfile)
        cfg = loader.get_single_data()
    yield cfg


@pytest.fixture(scope='session')
def root_dir() ->str:
    """
    Returns project's root dir
    @return: YAML object
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    yield root_dir + '/'


@pytest.fixture(scope='session')
def client():
    main.app.config['TESTING'] = True
    client = main.app.test_client()
    yield client