import os
from datetime import datetime

import pytz
from flasgger import Swagger
from flask import Flask, jsonify, Response

from app_name.utils import io
from app_name.utils.logger import logger, log
from app_name.utils.metric import Metric
from app_name.utils.monitoring import Monitoring
from app_name.utils.writers import CsvWriter

app = Flask(__name__)
config = io.load_config_by_env()
SCRIPT_START_TS = datetime.now(pytz.utc).isoformat()

# Obtener la ruta absoluta del archivo swagger.yaml
base_dir = os.path.abspath(os.path.dirname(__file__))  # Ruta de la carpeta src/
swagger_path = os.path.join(base_dir, '..', 'swagger.yaml')  # Subir un nivel y apuntar a swagger.yaml
# Configurar Swagger para que use el archivo swagger.yaml
swagger = Swagger(app, template_file=swagger_path)


@app.route("/", methods=['GET'])
def index() -> Response:
    """
    Un simple endpoint de bienvenida.
    ---
    responses:
      200:
        description: Respuesta exitosa
        examples:
          application/json: { "message": "Welcome message example" }
    """
    return jsonify({"message": "Welcome message example"})


def main():
    host = io.fetch_env_variable(config, 'HOST')
    port = io.fetch_env_variable(config, 'PORT')
    env = io.fetch_env_variable(config, 'APP_ENV')

    logger.info(log(f"Running the app on {host}:{port}"))

    monitoring = Monitoring(CsvWriter("metrics_example.csv"))
    # Add script common data to metric on development
    metric = Metric(app_env=env, process_name='app_name', script_name=os.path.basename(__file__),
                    root_process_type="FLASK", status="RUNNING", script_start_ts=SCRIPT_START_TS)
    monitoring.write_metric(metric)

    app.run(host=host, port=port)


if __name__ == '__main__':
    logger.debug(log("Starting the app..."))
    main()
