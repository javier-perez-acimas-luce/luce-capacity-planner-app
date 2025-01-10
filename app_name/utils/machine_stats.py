import json
import time

import psutil


class MachineStats:
    def __init__(self):
        self.refresh_stats()

    def refresh_stats(self):
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
        stats = self.get_stats(unit)
        return json.dumps(stats)


machine_stats = MachineStats()
