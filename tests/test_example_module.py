import pytest

import src.example.module as mod

from werkzeug.exceptions import BadRequest

def test_get_xml_ok(mocker, response):
    m = mocker.patch('src.example.module.requests.get')
    m.return_value = response
    result = mod.get_url_content("any_url")
    assert result.status_code == 200


def test_get_xml_connection_error(mocker, response):
    m = mocker.patch('src.example.module.requests.get')
    response.status_code = 400
    m.return_value = response
    with pytest.raises(BadRequest):
        mod.get_url_content("any_url")