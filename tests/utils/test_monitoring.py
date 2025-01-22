import pytest

from app_name.utils.metric import Metric
from app_name.utils.monitoring import Monitoring


@pytest.fixture
def mock_writer(mocker):
    return mocker.MagicMock()


@pytest.fixture
def monitoring(mock_writer):
    return Monitoring(writers=[mock_writer])


def test_write_metric(monitoring, mock_writer, mocker):
    metric = mocker.MagicMock(spec=Metric)
    monitoring.write_metric(metric)
    mock_writer.write.assert_called_once_with(metric.to_dict())


def test_write_metric_from_dict(monitoring, mock_writer):
    metric_data = {
        'app_env': 'test_env',
        'pipeline_id': '123',
        'pipeline_name': 'test_pipeline'
    }
    monitoring.write_metric_from_dict(metric_data)
    mock_writer.write.assert_called_once()
