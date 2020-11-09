import os

from flask import Flask, jsonify

from src.utils import io

app = Flask(__name__)
config = io.load_config(os.path.dirname(os.path.abspath(__file__)) + "/config.yaml")

@app.route("/")
def index() -> str:
    return jsonify({"message": "It Works"})

if __name__ == '__main__':
    # This is just for debugging
    app.run(host='0.0.0.0', port=80)