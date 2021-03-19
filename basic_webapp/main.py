import pkgutil

import yaml
from flask import Flask, jsonify

from basic_webapp.utils import io

app = Flask(__name__)
config = yaml.safe_load(pkgutil.get_data("data", "config.yaml"))


@app.route("/")
def index() -> str:
    return jsonify({"message": "XML Ingestion main page"})


if __name__ == '__main__':
    host = io.fetch_env_variable(config, 'HOST')
    port = io.fetch_env_variable(config, 'PORT')
    app.run(host=host, port=port)
