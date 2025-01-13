import json
import time

import psutil


class MachineStats:
    """
    MachineStats is responsible for collecting and providing system statistics.

    Attributes:
        cpu_count (int): The number of logical CPUs.
        cpu_freq (float): The current CPU frequency in MHz.
        virtual_memory (int): The total virtual memory in bytes.
        used_memory (int): The used virtual memory in bytes.
        free_memory (int): The available virtual memory in bytes.
        disk_usage (int): The total disk usage in bytes.
        used_disk (int): The used disk space in bytes.
        free_disk (int): The available disk space in bytes.
        net_io (psutil._common.snetio): The network I/O statistics.
        uptime (float): The system uptime in seconds.
    """

    def __init__(self):
        """
        Initializes the MachineStats instance and refreshes the statistics.
        """
        self.refresh_stats()

    def refresh_stats(self):
        """
        Refreshes the system statistics.
        """
        self.cpu_count = psutil.cpu_count(logical=True)
        self.cpu_freq = psutil.cpu_freq().current
        self.virtual_memory = psutil.virtual_memory().total
        self.used_memory = psutil.virtual_memory().used
        self.free_memory = psutil.virtual_memory().available
        self.disk_usage = psutil.disk_usage('/').total
        self.used_disk = psutil.disk_usage('/').used
        self.free_disk = psutil.disk_usage('/').free
        self.net_io = psutil.net_io_counters()
        self.uptime = time.time() - psutil.boot_time()

    def get_stats(self, unit='MB'):
        """
        Returns the system statistics in the specified unit.

        Args:
            unit (str): The unit for memory and disk statistics ('MB' or 'GB').

        Returns:
            dict: A dictionary containing the system statistics.
        """
        self.refresh_stats()
        if unit == 'GB':
            memory_divisor = 1024 ** 3
            memory_unit = 'GB'
        else:
            memory_divisor = 1024 ** 2
            memory_unit = 'MB'

        return {
            'cpu_count': f"{self.cpu_count} cores",
            'cpu_freq': f"{self.cpu_freq} MHz",
            'virtual_memory': f"{self.virtual_memory / memory_divisor:.3f} {memory_unit}",
            'used_memory': f"{self.used_memory / memory_divisor:.3f} {memory_unit}",
            'free_memory': f"{self.free_memory / memory_divisor:.3f} {memory_unit}",
            'disk_usage': f"{self.disk_usage / memory_divisor:.3f} {memory_unit}",
            'used_disk': f"{self.used_disk / memory_divisor:.3f} {memory_unit}",
            'free_disk': f"{self.free_disk / memory_divisor:.3f} {memory_unit}",
            'bytes_sent': f"{self.net_io.bytes_sent / memory_divisor:.3f} {memory_unit}",
            'bytes_recv': f"{self.net_io.bytes_recv / memory_divisor:.3f} {memory_unit}",
            'uptime': f"{self.uptime / 3600:.2f} hours"
        }

    def stats_to_message(self, unit='MB'):
        """
        Converts the system statistics to a JSON string.

        Args:
            unit (str): The unit for memory and disk statistics ('MB' or 'GB').

        Returns:
            str: A JSON string containing the system statistics.
        """
        stats = self.get_stats(unit)
        return json.dumps(stats)


machine_stats = MachineStats()
