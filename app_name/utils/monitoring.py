from typing import Optional, Union, List, Dict

from .metric import Metric
from .writers import Writer


class Monitoring:
    """
    Monitoring class that uses different writer classes to write metrics to various destinations.
    """

    def __init__(self, writers: Optional[Union[Writer, List[Writer]]]):
        """
        Initializes the Monitoring with the given writer(s).

        Args:
            writers (Optional[Union[object, List[object]]]): The writer instance or list of writer instances.
        """
        if writers is None:
            self.writers = []
        elif isinstance(writers, list):
            self.writers = writers
        else:
            self.writers = [writers]

    def write_metric(self, metric: Metric):
        """
        Writes the metric using the specified writers.

        Args:
            metric (Metric): The Metric instance to write.
        """
        metric.update_from_env()
        metric.update_timestamp()
        metric.update_machine_stats()
        for writer in self.writers:
            writer.write(metric.to_dict())

    def write_metric_from_dict(self, metric_data: Dict):
        """
        Writes the metric using the specified writers from a dictionary.

        Args:
            metric_data (Dict): The metric data to write.
        """
        metric = Metric(**metric_data)
        self.write_metric(metric)
