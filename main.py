import os

from flask import Flask, jsonify

from src.utils import io

app = Flask(__name__)
config = io.load_config(os.path.dirname(os.path.abspath(__file__)) + "/config.yaml")

@app.route("/")
def index() -> str:
    return jsonify({"message": "XML Ingestion main page"})

if __name__ == '__main__':
    host = io.fetch_env_variable(config, 'HOST')
    port = io.fetch_env_variable(config, 'PORT')
    app.run(host=host, port=port)