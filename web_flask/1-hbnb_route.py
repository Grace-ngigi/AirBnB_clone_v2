#!/usr/bin/python3
"""
Start a flask web app
running on localhost
listening t port 5000
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """ display Hello HBNB! """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ dusplay HBNB """
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
