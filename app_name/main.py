import os
from datetime import datetime

import pytz
from flask import Flask, jsonify, Response

from app_name.utils import io
from app_name.utils.logger import logger, log
from app_name.utils.metric import Metric
from app_name.utils.monitoring import Monitoring
from app_name.utils.writers import CsvWriter

app = Flask(__name__)
config = io.load_config_by_env()
SCRIPT_START_TS = datetime.now(pytz.utc).isoformat()


@app.route("/")
def index() -> Response:
    return jsonify({"message": "Welcome message example"})


def main():
    host = io.fetch_env_variable(config, 'HOST')
    port = io.fetch_env_variable(config, 'PORT')
    env = io.fetch_env_variable(config, 'APP_ENV')

    logger.info(log(f"Running the app on {host}:{port}"))

    monitoring = Monitoring(CsvWriter("logs/metrics_example.csv"))
    # Add script common data to metric on development
    metric = Metric(app_env=env, process_name='app_name', script_name=os.path.basename(__file__),
                    root_process_type="FLASK", status="RUNNING", script_start_ts=SCRIPT_START_TS)
    monitoring.write_metric(metric)

    app.run(host=host, port=port)


if __name__ == '__main__':
    logger.debug(log("Starting the app..."))
    main()
