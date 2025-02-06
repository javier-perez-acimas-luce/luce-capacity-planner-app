"""
This module provides various writer classes for writing metrics to different destinations, including files, databases, and queues.

Classes:
    Writer: Abstract base class for writing metrics.
    FileWriter: Writes metrics to a file.
    ParquetWriter: Writes metrics to a .parquet file.
    CsvWriter: Writes metrics to a CSV file.
    DBWriter: Writes metrics to a database.
    QueueWriter: Writes metrics to a queue.
"""
import json
import logging
import os
from abc import ABC, abstractmethod

import pandas as pd


class Writer(ABC):
    """
    Interfaz de clase Writer para escribir métricas.
    """
    base_path = 'logs/'

    @abstractmethod
    def write(self, metric):
        pass

    def set_base_path(self, base_path):
        self.base_path = base_path

    def create_base_path(self):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)


class FileWriter(Writer):
    """
    FileWriter class to write metrics to a file.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.logger = logging.getLogger('Monitoring')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(file_path)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

    def write(self, metric):
        self.logger.info(json.dumps(metric))


class ParquetWriter(Writer):
    """
    ParquetWriter class to write metrics to a .parquet file.
    """

    def __init__(self, file_path):
        self.file_path = super().base_path + file_path
        super().create_base_path()

    def write(self, metric):
        df = pd.DataFrame([metric])
        df.to_parquet(self.file_path, index=False, engine='pyarrow', compression='snappy')


class CsvWriter(Writer):
    """
    CsvWriter class to write metrics to a CSV file using pandas.
    """

    def __init__(self, file_path):
        self.file_path = super().base_path + file_path
        super().create_base_path()

    def write(self, metric):
        df = pd.DataFrame([metric])
        df.to_csv(self.file_path, mode='a', header=not pd.io.common.file_exists(self.file_path), index=False)


class DBWriter(Writer):
    """
    DBWriter class to write metrics to a database.
    """

    def __init__(self, db_client):
        # TODO: Implement database client
        self.db_client = db_client

    def write(self, metric):
        # TODO: Implement database insert
        self.db_client.insert(metric)


class QueueWriter(Writer):
    """
    QueueWriter class to write metrics to a queue.
    """

    def __init__(self, queue_client):
        # TODO: Implement queue client
        self.queue_client = queue_client

    def write(self, metric):
        # TODO: Implement queue send
        self.queue_client.send(json.dumps(metric))
