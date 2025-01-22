import os
from datetime import datetime

import pytz

from .machine_stats import MachineStats


class Metric:
    """
    Metric class to encapsulate metric data and provide methods to update and retrieve the data.
    """

    DEFAULT_SCHEMA = {
        'app_env': None,  # The application environment (e.g., 'pro', 'dev', 'uat')
        'pipeline_id': None,  # The unique identifier for the pipeline
        'pipeline_name': None,  # The name of the pipeline
        'script_id': None,  # The unique identifier for the script
        'script_name': None,  # The name of the script
        'process_id': os.getpid(),  # The process ID of the running script
        'trigger_type': None,  # The type of trigger that started the pipeline (e.g., 'manual', 'scheduled')
        'trigger_name': None,  # The name of the trigger
        'root_process_type': None,  # The type of the root process (e.g., 'raw', 'master', 'analytic', 'validation')
        'operation_type': None,
        # The type of operation being performed (e.g., 'read', 'write', 'transform', 'validation')
        'function_name': None,  # The name of the function being executed
        'rows': None,  # The number of rows processed
        'previous_rows': None,  # The number of rows processed in the last operation
        'path': None,  # The file of the operation
        'src_paths': None,  # The source file paths of the script
        'target_paths': None,  # The target file paths of the script
        'min_business_date': None,  # The minimum business date in the data
        'max_business_date': None,  # The maximum business date in the data
        'pipeline_status': None,  # The status of the pipeline (e.g., 'running', 'completed', 'failed')
        'message': None,  # A message describing the current state or event
        'timestamp': None,  # The timestamp of the metric
        'timezone': None,  # The timezone of the timestamp
        'execution_date': None,  # The date of execution
        'pipeline_start_ts': None,  # The timestamp when the pipeline started
        'pipeline_end_ts': None,  # The timestamp when the pipeline ended (if applicable)
        'machine_stats': None,  # The machine statistics (e.g., CPU, memory usage)
        'var1': None,  # Additional variable 1
        'var2': None,  # Additional variable 2
        'var3': None  # Additional variable 3
    }

    def __init__(self, app_env=None, pipeline_id=None, pipeline_name=None, script_id=None, script_name=None,
                 trigger_type=None, trigger_name=None, root_process_type=None, operation_type=None,
                 function_name=None, rows=None, previous_rows=None, path=None, src_paths=None,
                 target_paths=None, min_business_date=None, max_business_date=None, pipeline_status=None,
                 message=None, var1=None, var2=None, var3=None):
        """
        Initializes the Metric with the given data.

        Args:
            app_env (str, optional): The application environment.
            pipeline_id (str, optional): The unique identifier for the pipeline.
            pipeline_name (str, optional): The name of the pipeline.
            script_id (str, optional): The unique identifier for the script.
            script_name (str, optional): The name of the script.
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
            'var1': var1,
            'var2': var2,
            'var3': var3
        })
        self.machine_stats = MachineStats()
        self.update_from_env()
        self.update_timestamp()
        self.update_machine_stats()

    def update_with_dict(self, data):
        """
        Updates the metric data with a dictionary.

        Args:
            data (dict): The data to update the metric with.
        """
        self.data.update(data)
        self.update_from_env()
        self.update_timestamp()
        self.update_machine_stats()

    def update_with_params(self, app_env=None, pipeline_id=None, pipeline_name=None, script_id=None, script_name=None,
                           trigger_type=None, trigger_name=None, root_process_type=None, operation_type=None,
                           function_name=None, rows=None, previous_rows=None, path=None, src_paths=None,
                           target_paths=None, min_business_date=None, max_business_date=None, pipeline_status=None,
                           message=None, var1=None, var2=None, var3=None):
        """
        Updates the metric data with individual parameters.
        Be careful with this method, as it can overwrite existing data but don't delete it (use update_with_dict instead).

        Args:
            app_env (str, optional): The application environment.
            pipeline_id (str, optional): The unique identifier for the pipeline.
            pipeline_name (str, optional): The name of the pipeline.
            script_id (str, optional): The unique identifier for the script.
            script_name (str, optional): The name of the script.
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
            var1 (str, optional): Additional variable 1.
            var2 (str, optional): Additional variable 2.
            var3 (str, optional): Additional variable 3.
        """
        if app_env is not None:
            self.data['app_env'] = app_env
        if pipeline_id is not None:
            self.data['pipeline_id'] = pipeline_id
        if pipeline_name is not None:
            self.data['pipeline_name'] = pipeline_name
        if script_id is not None:
            self.data['script_id'] = script_id
        if script_name is not None:
            self.data['script_name'] = script_name
        if trigger_type is not None:
            self.data['trigger_type'] = trigger_type
        if trigger_name is not None:
            self.data['trigger_name'] = trigger_name
        if root_process_type is not None:
            self.data['root_process_type'] = root_process_type
        if operation_type is not None:
            self.data['operation_type'] = operation_type
        if function_name is not None:
            self.data['function_name'] = function_name
        if rows is not None:
            self.data['rows'] = rows
        if previous_rows is not None:
            self.data['previous_rows'] = previous_rows
        if path is not None:
            self.data['path'] = path
        if src_paths is not None:
            self.data['src_paths'] = src_paths
        if target_paths is not None:
            self.data['target_paths'] = target_paths
        if min_business_date is not None:
            self.data['min_business_date'] = min_business_date
        if max_business_date is not None:
            self.data['max_business_date'] = max_business_date
        if pipeline_status is not None:
            self.data['pipeline_status'] = pipeline_status
        if message is not None:
            self.data['message'] = message
        if var1 is not None:
            self.data['var1'] = var1
        if var2 is not None:
            self.data['var2'] = var2
        if var3 is not None:
            self.data['var3'] = var3

        self.update_from_env()
        self.update_timestamp()
        self.update_machine_stats()

    def update_timestamp(self):
        """
        Updates the timestamp and timezone in the metric data.
        """
        now = datetime.now(pytz.utc)
        self.data['timestamp'] = now.isoformat()
        self.data['timezone'] = str(now.tzinfo)
        self.data['execution_date'] = now.date().isoformat()

    def update_machine_stats(self):
        """
        Updates the timestamp and timezone in the metric data.
        """
        self.machine_stats.refresh_stats()
        self.data['machine_stats'] = self.machine_stats.stats_to_message(unit='GB')

    def update_from_env(self):
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

    def to_dict(self):
        """
        Returns the metric data as a dictionary.

        Returns:
            dict: The metric data.
        """
        return self.data
