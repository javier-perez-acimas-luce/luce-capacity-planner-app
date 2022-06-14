import pkgutil

import yaml
from flask import Flask, jsonify, Response

from app_name.utils import io

app = Flask(__name__)
config = yaml.safe_load(pkgutil.get_data("data", "config.yaml"))


@app.route("/")
def index() -> Response:
    return jsonify({"message": "Welcome message example"})


def main():
    host = io.fetch_env_variable(config, 'HOST')
    port = io.fetch_env_variable(config, 'PORT')
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
