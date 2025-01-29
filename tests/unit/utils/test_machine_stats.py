import pytest

from app_name.utils.machine_stats import MachineStats


@pytest.fixture
def machine_stats():
    return MachineStats()


def test_refresh_stats(machine_stats, mocker):
    mock_psutil = mocker.patch('app_name.utils.machine_stats.psutil')
    mock_psutil.cpu_count.return_value = 4
    mock_psutil.virtual_memory.return_value = mocker.MagicMock(total=8, available=4)
    machine_stats.refresh_stats()
    assert machine_stats.cpu_count == 4
    assert machine_stats.virtual_memory == 8
    assert machine_stats.free_memory == 4
