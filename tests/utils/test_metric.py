import pytest

from app_name.utils.metric import Metric


@pytest.fixture
def metric():
    return Metric(app_env='dev', pipeline_id='123', pipeline_name='test_pipeline')


def test_initialization(metric):
    assert metric.data['app_env'] == 'dev'
    assert metric.data['pipeline_id'] == '123'
    assert metric.data['pipeline_name'] == 'test_pipeline'


def test_update_with_dict(metric):
    update_data = {'app_env': 'prod', 'pipeline_id': '456'}
    metric.update_with_dict(update_data)
    assert metric.data['app_env'] == 'prod'
    assert metric.data['pipeline_id'] == '456'


def test_update_timestamp(mocker, metric):
    mock_datetime = mocker.patch('app_name.utils.metric.datetime')
    mock_pytz = mocker.patch('app_name.utils.metric.pytz')
    mock_now = mocker.MagicMock()
    mock_now.isoformat.return_value = '2023-01-01T00:00:00+00:00'
    mock_now.date.return_value.isoformat.return_value = '2023-01-01'
    mock_pytz.utc = 'UTC'
    mock_now.tzinfo = 'UTC'
    mock_datetime.now.return_value = mock_now

    metric._update_timestamp()
    assert metric.data['timestamp'] == '2023-01-01T00:00:00+00:00'
    assert metric.data['timezone'] == 'UTC'
    assert metric.data['execution_date'] == '2023-01-01'


def test_update_from_env(mocker, metric):
    mocker.patch.dict('os.environ', {'APP_ENV': 'test_env', 'LOG_TIMEZONE': 'UTC'})
    metric.data['app_env'] = None
    metric.data['timezone'] = None
    metric._update_from_env()
    assert metric.data['app_env'] == 'test_env'
    assert metric.data['timezone'] == 'UTC'
