import os

from flask import Flask, Response
from markupsafe import escape

from db.db import db
from util.logger import get_logger
from route.credential_list_routes import credential_list_blueprint

basedir = os.path.abspath(os.path.dirname(__file__))
logger = get_logger(__name__)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'db', 'hibp.sqlite3')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()


app.register_blueprint(credential_list_blueprint)

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

@app.route("/<name>")
def hello_name(name):
    return name

if __name__ == "__main__":
    app.run(debug=True)