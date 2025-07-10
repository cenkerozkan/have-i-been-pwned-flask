from flask import Flask
from markupsafe import escape
from util.logger import get_logger

logger = get_logger(__name__)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

@app.route("/<name>")
def hello_name(name):
    logger.info(f"Hello {name}")
    return escape(name)