from flask import Flask, jsonify, Response

from app_name.utils import io
from app_name.utils.logger import logger, log

app = Flask(__name__)
config = io.load_config_by_env()

@app.route("/")
def index() -> Response:
    return jsonify({"message": "Welcome message example"})


def main():
    host = io.fetch_env_variable(config, 'HOST')
    port = io.fetch_env_variable(config, 'PORT')
    logger.info(log(f"Running the app on {host}:{port}"))
    app.run(host=host, port=port)


if __name__ == '__main__':
    logger.debug(log("Starting the app..."))
    main()
