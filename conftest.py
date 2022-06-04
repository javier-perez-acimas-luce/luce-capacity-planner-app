
import os

import pytest
import requests
import yaml

from app_name import main


@pytest.fixture
def config() -> yaml:
    """
    Creates a config file object to run the tests
    @return: YAML object
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = root_dir + '/data/config.yaml'
    with open(config_path, 'r') as ymlfile:
        loader = yaml.Loader(ymlfile)
        cfg = loader.get_single_data()
    yield cfg


@pytest.fixture(scope='session')
def root_dir() -> str:
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


@pytest.fixture
def response():
    response = requests.Response()
    response.status_code = 200
    response.url = "www.something.com/data.xml"
    response._content = b'<?xml version="1.0" encoding="iso-8859-1" standalone="yes" ?><Config></Config>'
    return response
