import flask
import pytest
from werkzeug.exceptions import Forbidden, BadRequest

from app_name.utils import requests


def test_validate_token_wrong_token(config):
    with pytest.raises(Forbidden):
        app = flask.Flask(__name__)
        with app.test_request_context('/ingestion/xml?token=bad'):
            requests.validate_token(flask.request, config)


def test_validate_token_missing_token(config):
    with pytest.raises(Forbidden):
        app = flask.Flask(__name__)
        with app.test_request_context('/ingestion/xml'):
            requests.validate_token(flask.request, config)


def test_validate_token(config):
    app = flask.Flask(__name__)
    with app.test_request_context('/ingestion/xml?token='+config['token']):
        status = requests.validate_token(flask.request, config)
        assert status is True


def test_validate_request():
    app = flask.Flask(__name__)
    with app.test_request_context('/ingestion/xml?field1=value1&field2=value2'):
        params = requests.validate_request(flask.request, ['field1', 'field2'])
        assert 'field1', 'field2' in params.keys()
        assert 'value1', 'value2' in params.values()


def test_validate_request_with_optional_field():
    app = flask.Flask(__name__)
    with app.test_request_context('/ingestion/xml?field1=value1&field2=value2&field3=value3'):
        params = requests.validate_request(flask.request, ['field1', 'field2'])
        assert 'field3' not in params.keys()


def test_validate_request_raises_bad_request():
    with pytest.raises(BadRequest):
        app = flask.Flask(__name__)
        with app.test_request_context('/ingestion/xml?field3=value3'):
            requests.validate_request(flask.request, ['field1', 'field2'])
