from flask import Flask
from markupsafe import escape
from util.logger import get_logger

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

@app.route("/<name>")
def hello_name(name):
    return name

if __name__ == "__main__":
    app.run(debug=True)