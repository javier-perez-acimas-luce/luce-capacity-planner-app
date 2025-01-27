"""
This module provides the Metric class for encapsulating metric data and methods to update and retrieve the data.

Classes:
    Metric: Encapsulates metric data and provides methods to update and retrieve the data..

Functions:
    update_with_dict(data): Updates the metric data with a dictionary.
    update_with_params(...): Updates the metric data with individual parameters.
    _update_data(params): Updates the metric data with the provided parameters.
    _update_timestamp(): Updates the timestamp and timezone in the metric data.
    _update_machine_stats(): Updates the machine statistics in the metric data.
    _update_from_env(): Updates the metric data with values from environment variables if they are not provided.
    to_dict(update=True): Returns the metric data as a dictionary.
"""
import os
from datetime import datetime

import pytz

from .machine_stats import MachineStats


class Metric(object):
    """
    Metric class to encapsulate metric data and provide methods to update and retrieve the data.
    """

    DEFAULT_SCHEMA = {
        # The application environment (e.g., 'pro', 'dev', 'uat')
        'app_env': None,
        # The unique identifier for the pipeline
        'pipeline_id': None,
        # The name of the pipeline
        'pipeline_name': None,
        # The unique identifier for the script
        'script_id': None,
        # The name of the script
        'script_name': None,
        # The process ID of the running script
        'process_id': os.getpid(),
        # The name of the process
        'process_name': None,
        # The type of trigger that started the pipeline (e.g., 'manual', 'scheduled')
        'trigger_type': None,
        # The name of the trigger
        'trigger_name': None,
        # The type of the root process (e.g., 'raw', 'master', 'analytic', 'validation')
        'root_process_type': None,
        # The type of operation being performed (e.g., 'read', 'write', 'transform', 'validation')
        'operation_type': None,
        # The name of the function being executed
        'function_name': None,
        # The number of rows processed
        'rows': None,
        # The number of rows processed in the last operation
        'previous_rows': None,
        # The file of the operation
        'path': None,
        # The source file paths of the script
        'src_paths': None,
        # The target file paths of the script
        'target_paths': None,
        # The minimum business date in the data
        'min_business_date': None,
        # The maximum business date in the data
        'max_business_date': None,
        # The status of the pipeline (e.g., 'running', 'completed', 'failed')
        'pipeline_status': None,
        # A message describing the current state or event
        'message': None,
        # The timestamp of the metric
        'timestamp': None,
        # The timezone of the timestamp
        'timezone': None,
        # The date of execution
        'execution_date': None,
        # The timestamp when the pipeline started
        'pipeline_start_ts': None,
        # The timestamp when the pipeline ended (if applicable)
        'pipeline_end_ts': None,
        # The timestamp when the script started
        'script_start_ts': None,
        # The timestamp when the script ended (if applicable)
        'script_end_ts': None,
        # The machine statistics (e.g., CPU, memory usage)
        'machine_stats': None,
        # Additional variable 1
        'var1': None,
        # Additional variable 2
        'var2': None,
        # Additional variable 3
        'var3': None
    }

    def __init__(self, app_env=None, pipeline_id=None, pipeline_name=None, script_id=None, script_name=None,
                 process_name=None, trigger_type=None, trigger_name=None, root_process_type=None, operation_type=None,
                 function_name=None, rows=None, previous_rows=None, path=None, src_paths=None,
                 target_paths=None, min_business_date=None, max_business_date=None, pipeline_status=None,
                 message=None, pipeline_start_ts=None, pipeline_end_ts=None, script_start_ts=None,
                 script_end_ts=None, var1=None, var2=None, var3=None):
        """
        Initializes the Metric with the given data.

        Args:
            app_env (str, optional): The application environment.
            pipeline_id (str, optional): The unique identifier for the pipeline.
            pipeline_name (str, optional): The name of the pipeline.
            script_id (str, optional): The unique identifier for the script.
            script_name (str, optional): The name of the script.
            process_name (str, optional): The name of the process.
            trigger_type (str, optional): The type of trigger that started the pipeline.
            trigger_name (str, optional): The name of the trigger.
            root_process_type (str, optional): The type of the root process.
            operation_type (str, optional): The type of operation being performed.
            function_name (str, optional): The name of the function being executed.
            rows (int, optional): The number of rows processed.
            previous_rows (int, optional): The number of rows processed in the last operation.
            path (str, optional): The file of the operation.
            src_paths (list, optional): The source file paths of the script.
            target_paths (list, optional): The target file paths of the script.
            min_business_date (str, optional): The minimum business date in the data.
            max_business_date (str, optional): The maximum business date in the data.
            pipeline_status (str, optional): The status of the pipeline.
            message (str, optional): A message describing the current state or event.
            pipeline_start_ts (datetime.datime,optional): The timestamp when the pipeline started
            pipeline_end_ts (datetime.datetime,optional): The timestamp when the pipeline ended (if applicable)
            script_start_ts (datetime.datime,optional): The timestamp when the script started
            script_end_ts (datetime.datetime,optional): The timestamp when the script ended (if applicable)
            var1 (str, optional): Additional variable 1.
            var2 (str, optional): Additional variable 2.
            var3 (str, optional): Additional variable 3.
        """
        self.data = self.DEFAULT_SCHEMA.copy()
        self.data.update({
            'app_env': app_env,
            'pipeline_id': pipeline_id,
            'pipeline_name': pipeline_name,
            'script_id': script_id,
            'script_name': script_name,
            'process_name': process_name,
            'trigger_type': trigger_type,
            'trigger_name': trigger_name,
            'root_process_type': root_process_type,
            'operation_type': operation_type,
            'function_name': function_name,
            'rows': rows,
            'previous_rows': previous_rows,
            'path': path,
            'src_paths': src_paths,
            'target_paths': target_paths,
            'min_business_date': min_business_date,
            'max_business_date': max_business_date,
            'pipeline_status': pipeline_status,
            'message': message,
            'pipeline_start_ts': pipeline_start_ts,
            'pipeline_end_ts': pipeline_end_ts,
            'script_start_ts': script_start_ts,
            'script_end_ts': script_end_ts,
            'var1': var1,
            'var2': var2,
            'var3': var3
        })
        self.machine_stats = MachineStats()
        self._update_from_env()
        self._update_timestamp()
        self._update_machine_stats()

    def update_with_dict(self, data):
        """
        Updates the metric data with a dictionary.

        Args:
            data (dict): The data to update the metric with.

        Returns:
            Metric: The Metric instance.
        """
        self.data.update(data)
        self._update_from_env()
        self._update_timestamp()
        self._update_machine_stats()
        return self

    def update_with_params(self, app_env=None, pipeline_id=None, pipeline_name=None, script_id=None, script_name=None,
                           process_name=None, trigger_type=None, trigger_name=None, root_process_type=None,
                           operation_type=None, function_name=None, rows=None, previous_rows=None, path=None,
                           src_paths=None,
                           target_paths=None, min_business_date=None, max_business_date=None, pipeline_status=None,
                           message=None, pipeline_start_ts=None, pipeline_end_ts=None, script_start_ts=None,
                           script_end_ts=None, var1=None, var2=None, var3=None):
        """
        Updates the metric data with individual parameters.
        Be careful with this method, as it can overwrite existing data but don't delete it (use update_with_dict instead).

        Args:
            app_env (str, optional): The application environment.
            pipeline_id (str, optional): The unique identifier for the pipeline.
            pipeline_name (str, optional): The name of the pipeline.
            script_id (str, optional): The unique identifier for the script.
            script_name (str, optional): The name of the script.
            process_name (str, optional): The name of the process.
            trigger_type (str, optional): The type of trigger that started the pipeline.
            trigger_name (str, optional): The name of the trigger.
            root_process_type (str, optional): The type of the root process.
            operation_type (str, optional): The type of operation being performed.
            function_name (str, optional): The name of the function being executed.
            rows (int, optional): The number of rows processed.
            previous_rows (int, optional): The number of rows processed in the last operation.
            path (str, optional): The file of the operation.
            src_paths (list, optional): The source file paths of the script.
            target_paths (list, optional): The target file paths of the script.
            min_business_date (str, optional): The minimum business date in the data.
            max_business_date (str, optional): The maximum business date in the data.
            pipeline_status (str, optional): The status of the pipeline.
            message (str, optional): A message describing the current state or event.
            pipeline_start_ts (datetime.datime,optional): The timestamp when the pipeline started
            pipeline_end_ts (datetime.datetime,optional): The timestamp when the pipeline ended (if applicable)
            script_start_ts (datetime.datime,optional): The timestamp when the script started
            script_end_ts (datetime.datetime,optional): The timestamp when the script ended (if applicable)
            var1 (str, optional): Additional variable 1.
            var2 (str, optional): Additional variable 2.
            var3 (str, optional): Additional variable 3.

        Returns:
            Metric: The Metric instance.
        """
        params = {
            'app_env': app_env,
            'pipeline_id': pipeline_id,
            'pipeline_name': pipeline_name,
            'script_id': script_id,
            'script_name': script_name,
            'process_name': process_name,
            'trigger_type': trigger_type,
            'trigger_name': trigger_name,
            'root_process_type': root_process_type,
            'operation_type': operation_type,
            'function_name': function_name,
            'rows': rows,
            'previous_rows': previous_rows,
            'path': path,
            'src_paths': src_paths,
            'target_paths': target_paths,
            'min_business_date': min_business_date,
            'max_business_date': max_business_date,
            'pipeline_status': pipeline_status,
            'message': message,
            'pipeline_start_ts': pipeline_start_ts,
            'pipeline_end_ts': pipeline_end_ts,
            'script_start_ts': script_start_ts,
            'script_end_ts': script_end_ts,
            'var1': var1,
            'var2': var2,
            'var3': var3
        }

        self._update_data(params)
        self._update_from_env()
        self._update_timestamp()
        self._update_machine_stats()

        return self

    def _update_data(self, params):
        """
        Updates the metric data with the provided parameters.

        Args:
            params (dict): The parameters to update the metric data with.
        """
        for key, value in params.items():
            if value is not None:
                self.data[key] = value

    def _update_timestamp(self):
        """
        Updates the timestamp and timezone in the metric data.
        """
        now = datetime.now(pytz.utc)
        self.data['timestamp'] = now.isoformat()
        self.data['timezone'] = str(now.tzinfo)
        self.data['execution_date'] = now.date().isoformat()

    def _update_machine_stats(self):
        """
        Updates the timestamp and timezone in the metric data.
        """
        self.machine_stats.refresh_stats()
        self.data['machine_stats'] = self.machine_stats.stats_to_message(unit='GB')

    def _update_from_env(self):
        """
        Updates the metric data with values from environment variables if they are not provided.
        """
        env_vars = {
            'app_env': 'APP_ENV',
            'timezone': 'LOG_TIMEZONE'
        }
        for key, env_var in env_vars.items():
            if self.data.get(key) is None:
                self.data[key] = os.getenv(env_var)

    def to_dict(self, new_values=None, update=True):
        """
        Returns the metric data as a dictionary, optionally applying temporary changes.

        Args:
            new_values (dict, optional): Temporary changes to apply to the metric data.
            update (bool): Whether to update the metric data before returning it.

        Returns:
            dict: The metric data.
        """
        if update:
            self._update_from_env()
            self._update_timestamp()
            self._update_machine_stats()

        data_copy = self.data.copy()

        if new_values:
            data_copy.update(new_values)

        return data_copy
