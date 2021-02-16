import pytest

def test_index(client):
    response = client.get('/')
    result = response.get_json()
    assert result is not None
    assert "message" in result